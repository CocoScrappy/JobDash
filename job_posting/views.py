from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.corpus import stopwords
import sys
from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from . import serializers
from rest_framework.decorators import action
from .models import JobPost, Skill
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.serializers import serialize
import json
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination
from cv_basic.models import CvBasic
from . import compare_html
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import requests
import html2text
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from operator import attrgetter

sp = spacy.load('en_core_web_sm')
spacy_stopwords = set(sp.Defaults.stop_words)
nltk_stopwords = set(nltk.corpus.stopwords.words('english'))

stop_words = spacy_stopwords.union(nltk_stopwords.union(ENGLISH_STOP_WORDS))
stop_words = set(stop_words)
nltk.download('stopwords')

# Create your views here.


def extract_text_from_docx(html):
    h = html2text.HTML2Text()
    h.ignore_links = True
    txt = h.handle(html)
    if txt:
        txt = txt.lower()
        return txt.replace('\t', ' ')
    return None


def get_matching_skills(input_text, skills):
    skills = set(skills)

    # stop_words = set(nltk.corpus.stopwords.words('english'))
    # word_tokens = nltk.tokenize.word_tokenize(input_text)

    # # remove the stop words
    # filtered_tokens = [w for w in word_tokens if w not in stop_words]

    # # remove the punctuation
    # filtered_tokens = [w for w in word_tokens if w.isalpha()]

    # # generate bigrams and trigrams (such as artificial intelligence)
    # bigrams_trigrams = list(
    #     map(' '.join, nltk.everygrams(filtered_tokens, 2, 2)))

    vectorizer = CountVectorizer(stop_words=stop_words, ngram_range=(1, 2))
    X = vectorizer.fit_transform([input_text])
    word_tokens = vectorizer.get_feature_names_out()

    # we create a set to keep the results in.
    found_skills = set()

    # we search for each token in our skills
    for token in word_tokens:
        if token.lower() in skills:
            found_skills.add(token.lower())

    not_found_skills = set(skills.difference(found_skills))

    return {'found_skills': found_skills, 'missing_skills': not_found_skills}


def skill_exists(skill):
    try:
        url = f'https://api.apilayer.com/skills?q={skill}&amp;count=1'
        headers = {'apikey': 'KWmvnGBqLYTccSspokYbOOwIeLBUd9XB'}
        response = requests.request('GET', url, headers=headers)
        result = response.json()
        # print(response)
        # print(result)

        if len(result) > 0:
            for result_skill in result:
                Skill.objects.create(name=result_skill)
            return result[0].lower() == skill.lower()
        else:
            Skill.objects.create(name=skill, isSkill=False)
    except Exception as e:
        return True


def extract_skills(input_text):
    # stop_words = set(nltk.corpus.stopwords.words('english'))
    vectorizer = CountVectorizer(stop_words=stop_words)
    X = vectorizer.fit_transform([input_text])
    word_tokens = vectorizer.get_feature_names_out()
    word_tokens = set(word_tokens)

    db_skills = Skill.objects.filter(
        isSkill=True).values_list('name', flat=True)
    db_tokens = Skill.objects.all().values_list('name', flat=True)

    # word_tokens = nltk.tokenize.word_tokenize(input_text)

    # remove the stop words
    # filtered_tokens = [w for w in word_tokens if w not in stop_words]

    # # remove the punctuation
    # filtered_tokens = [w for w in word_tokens if w.isalpha()]
    # filtered_tokens = [w.lower() for w in word_tokens]

    # generate bigrams and trigrams (such as artificial intelligence)
    # bigrams_trigrams = list(
    #     map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

    # we create a set to keep the results in.

    required_skills = word_tokens.intersection(db_skills)
    tokens_not_in_db = word_tokens.difference(db_tokens)

    # we search for each token in our skills database
    for token in tokens_not_in_db:
        if skill_exists(token.lower()):
            required_skills.add(token.lower())

    # we search for each bigram and trigram in our skills database
    # for ngram in bigrams_trigrams:
    #     if skill_exists(ngram.lower()):
    #         found_skills.add(ngram.lower())

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

        #jsonquery = json.loads(DefaultJobPostSerializer(query).data)

        print(searchTerms, file=sys.stderr)
        return LimitOffsetPagination.get_paginated_response(self, responseQuery)
        # return Response(jsonquery, status=status.HTTP_200_OK)


class JobMatchView(APIView, LimitOffsetPagination):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args,):
        user = request.user
        jobId = request.data['jobId']

        resume = CvBasic.objects.get(user=user).content
        job_description = JobPost.objects.get(pk=jobId).description

        resume_text = extract_text_from_docx(resume)
        job_description_text = extract_text_from_docx(
            job_description)

        required_skills = extract_skills(job_description_text)
        required_skills = set(required_skills)
        # required_skills_text = ' '.join(required_skills)
        # text = [resume_text, required_skills_text]
        # matchPercentage = compare_html.get_text_matching_score(text)
        matching_skills_results = get_matching_skills(
            resume_text, required_skills)
        matching_score = len(
            matching_skills_results['found_skills'])*100/len(required_skills)
        matching_score = round(matching_score, 2)

        return Response({"matching_score": matching_score, 'matching_skills_results': matching_skills_results}, status=status.HTTP_200_OK)


class GetDbSkillsView(APIView, LimitOffsetPagination):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args,):

        db_skills = Skill.objects.filter(
            isSkill=True).values_list('name', flat=True)
        # db_skills_list = [skill['name'] for skill in db_skills_objects]

        return Response(db_skills, status=status.HTTP_200_OK)


class GetDbNotSkillTokensView(APIView, LimitOffsetPagination):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args,):
        db_skills = Skill.objects.filter(
            isSkill=False).values_list('name', flat=True)
        # db_skills_list = [skill['name'] for skill in db_skills_objects]

        return Response(db_skills, status=status.HTTP_200_OK)


class GetDbSkillTokensView(APIView, LimitOffsetPagination):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args,):

        db_skills = Skill.objects.all().values_list('name', flat=True)
        # db_skills_list = [skill['name'] for skill in db_skills_objects]

        return Response(db_skills, status=status.HTTP_200_OK)
