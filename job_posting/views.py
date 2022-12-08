import sys
from rest_framework import viewsets, status, permissions
from . import serializers
from rest_framework.decorators import action
from .models import JobPost, Skill
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination
from cv_basic.models import CvBasic
from . import compare_html
import requests
import html2text
from sklearn.feature_extraction.text import CountVectorizer
import os
from decouple import config
from django.db.models.functions import Lower


# Create your views here.

def extract_text_from_docx(html):
    h = html2text.HTML2Text()
    h.ignore_links = True
    txt = h.handle(html)
    if txt:
        txt = txt.lower()
        return txt.replace('\t', ' ')
    return None


def get_vectorized_word_tokens(input_text, ngram_range):
    vectorizer = CountVectorizer(
        stop_words=compare_html.STOP_WORDS, ngram_range=ngram_range)
    X = vectorizer.fit_transform([input_text])
    word_tokens = set(vectorizer.get_feature_names_out())
    return word_tokens


def get_matching_skills(cv_text, job_text):

    cv_tokens = set(get_vectorized_word_tokens(cv_text, (1, 2)))
    job_tokens = set(get_vectorized_word_tokens(job_text, (1, 2)))

    db_skills = Skill.objects.filter(
        isSkill=True).values_list('name', flat=True)

    # we create a set to keep the results in.
    required_skills = job_tokens.intersection(db_skills)
    matching_skills = required_skills.intersection(cv_tokens)

    missing_skills = required_skills.difference(cv_tokens)

    matching_score = len(matching_skills)*100/len(required_skills)
    matching_score = round(matching_score, 0)

    return {'matching_score': matching_score, 'matching_skills': matching_skills, 'missing_skills': missing_skills}


def skill_exists(skill, db_skills):
    try:
        url = f'https://api.apilayer.com/skills?q={skill}'
        headers = {'apikey': config('SKILLS_API_TOKEN')}
        response = requests.request('GET', url, headers=headers)
        # print(response)
        # print(result)
        # print(len(result))

        if response.status_code == 200:
            result = response.json()
            if len(result) > 0:
                result = set([skill.lower() for skill in result])
                result_skills_not_in_db = result.difference(db_skills)
                # print(result_skills_not_in_db)
                for result_skill in result_skills_not_in_db:
                    # print(result_skill)
                    Skill.objects.create(name=result_skill.lower())
                return result[0].lower() == skill.lower()
        return False
    except Exception as e:
        print('Error: ' + getattr(e, 'message', repr(e)))
        return False


def extract_skills(input_text):
    vectorizer = CountVectorizer(stop_words=compare_html.STOP_WORDS)
    X = vectorizer.fit_transform([input_text])
    word_tokens = vectorizer.get_feature_names_out()
    word_tokens = set(word_tokens)

    db_skills = Skill.objects.filter(
        isSkill=True).values_list('name', flat=True)
    db_tokens = Skill.objects.all().values_list('name', flat=True)

    required_skills = word_tokens.intersection(db_skills)
    tokens_not_in_db = word_tokens.difference(db_tokens)
    print("nb of tokens not in db: {}".format(len(tokens_not_in_db)))

    for token in tokens_not_in_db:
        if skill_exists(token.lower(), db_skills):
            print(token + " found in API")
            required_skills.add(token.lower())
            if (len(Skill.objects.filter(name=token.lower())) < 1):
                print(token + " storing in DB as skill")
                Skill.objects.create(name=token.lower())
                print(token + " saved in DB")
        else:
            print(token + " not in DB or API")
            if (len(Skill.objects.filter(name=token.lower())) < 1):
                print(token + " storing in DB as not skill")
                Skill.objects.create(name=token.lower(), isSkill=False)
                print(token + " saved in DB")

    return required_skills


class DefaultJobPostView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.DefaultJobPostSerializer
    queryset = JobPost.objects.all()


class JobPostView(viewsets.ModelViewSet):
    """
    For users : Gets all *internal* job postings.
    For employers: Get all *internal* job posting for that user via the auth token Id.
    Returns a paginated and serialized queryset with all the matches.

    **Context**

    ``def get_user_job_postings(self, request):``
    uses request.user to get authenticated user id from token

    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.JobPostSerializer
    pagination_class = LimitOffsetPagination
    queryset = JobPost.objects.all()

    @action(detail=False, methods=['get'], url_path="get_user_postings")
    def get_user_postings(self, request):

        try:
            user = request.user

            if (user.role == 'employer'):

                userPosts = JobPost.objects.filter(
                    employer=user.id).select_related("employer")
            else:
                userPosts = JobPost.objects.all()
            if not userPosts:
                return Response({"message": "No job postings found for current user",
                                 "data": []},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                data = []
                # pagination must happen before serialization
                userPosts = self.paginate_queryset(userPosts)
                for post in userPosts:

                    posting = self.get_serializer(post).data
                    data.append(posting)
                # print(data)
                return self.get_paginated_response(data)
                # return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(getattr(e, 'message', repr(e)))
            return Response({"message": "WHOOPS, and error occurred; " + getattr(e, 'message', repr(e))},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JobSearchView(APIView, LimitOffsetPagination):
    """
    Allows to search for *internal* job postings, related to :model:`job_posting.JobPost`, returns a paginated and serialized queryset with all the matches.

    **Context**

    ``def get(self, request, par, loc=None):``
        Takes in "par" as the search parameter, it can take several parameters. 
        Takes in "loc" as an optional parameter for the location. It will try to find matches with both :model:`job_posting.JobPost`'s remote_options and location.

    ``q = JobPost.objects.filter(Q(title__icontains=t) | Q(description__icontains=t))``
        Queries that match EITHER in the title OR in the description will be added to the Query Set

    ``if searchLocation != None:q=q.filter(Q(remote_option__icontains=loc)|Q(location__icontains=loc))``
        These queries will be trimmed to only include loc matches that match "remote_option" or "location". If no location was given, this step is skipped.

    """

    serializer_class = serializers.JobPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, par, loc=None):
        print(request.user, file=sys.stderr)
        user = request.user
        searchTerms = par.split()
        searchLocation = loc
        query = None
        for t in searchTerms:
            q = JobPost.objects.filter(
                Q(title__icontains=t) | Q(description__icontains=t))

            if searchLocation != None:
                q = q.filter(Q(remote_option__icontains=loc)
                             | Q(location__icontains=loc))

            if user.role == 'employer':
                q = q.filter(employer=user.id)

            if query == None:
                query = q
            else:
                query = query | q

        query = self.paginate_queryset(query, request, view=self)

        responseQuery = []
        for q in query:
            responseQuery.append(serializers.DefaultJobPostSerializer(q).data)

        print(searchTerms, file=sys.stderr)
        return LimitOffsetPagination.get_paginated_response(self, responseQuery)


class JobMatchView(APIView, LimitOffsetPagination):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args,):
        try:
            user = request.user
            jobId = request.data['jobId']

            resume = CvBasic.objects.get(user=user).content
            job_description = JobPost.objects.get(pk=jobId).description

            resume_text = extract_text_from_docx(resume)
            job_description_text = extract_text_from_docx(
                job_description)

            extracted_skills = extract_skills(job_description_text)
            # required_skills = set(required_skills)
            matching_skills_results = get_matching_skills(
                resume_text, job_description_text)

            return Response(matching_skills_results, status=status.HTTP_200_OK)
        except Exception as e:
            print(getattr(e, 'message', repr(e)))
            return Response({"message": "WHOOPS, and error occurred; " + getattr(e, 'message', repr(e))},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetDbSkillsView(APIView, LimitOffsetPagination):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args,):
        db_skills = Skill.objects.filter(
            isSkill=True).values_list('name', flat=True)
        return Response(db_skills, status=status.HTTP_200_OK)


class GetDbNotSkillTokensView(APIView, LimitOffsetPagination):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args,):
        db_skills = Skill.objects.filter(
            isSkill=False).values_list('name', flat=True)
        return Response(db_skills, status=status.HTTP_200_OK)


class GetDbSkillTokensView(APIView, LimitOffsetPagination):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args,):
        db_skills = Skill.objects.all().values_list('name', flat=True)
        return Response(db_skills, status=status.HTTP_200_OK)


class SkillsAPIView(APIView, LimitOffsetPagination):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args,):
        print(config('SKILLS_API_TOKEN'))
        skill = request.data['skill']
        db_skills = set(Skill.objects.filter(
            isSkill=True).values_list('name', flat=True))
        try:
            url = f'https://api.apilayer.com/skills?q={skill}'
            headers = {'apikey': config('SKILLS_API_TOKEN')}
            response = requests.request('GET', url, headers=headers)
            print(response)
            # print(result)
            # print(len(result))

            if response.status_code == 200:
                result = response.json()
                result = set([skill.lower() for skill in result])
                if len(result) > 0:
                    result_skills_not_in_db = result.difference(db_skills)
                    # print(result_skills_not_in_db)
                    for result_skill in result_skills_not_in_db:
                        # print(result_skill)
                        # if (len(Skill.objects.filter(name=result_skill)) < 1):
                        Skill.objects.create(name=result_skill.lower())
                    return Response(True, status=status.HTTP_200_OK)
                else:
                    if (len(Skill.objects.filter(name=skill)) < 1):
                        Skill.objects.create(name=skill.lower(), isSkill=False)
                    return Response(False, status=status.HTTP_200_OK)
            else:
                return Response(False, status=status.HTTP_200_OK)
        except Exception as e:
            print('Error: ' + getattr(e, 'message', repr(e)))
            return Response(False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SetDbSkillsLowerCaseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args,):
        try:
            Skill.objects.update(name=Lower('name'))
            return Response("Success", status=status.HTTP_200_OK)
        except Exception as e:
            print('Error: ' + getattr(e, 'message', repr(e)))
            return Response(False, status=status.HTTP_200_OK)
