from django.shortcuts import render
from rest_framework import viewsets, status, permissions
import sys
from user.models import UserAccount
from user.serializers import UserSerializer
from . import serializers
from .models import Application
from cv_basic.models import CvBasic
from cv_basic.serializers import DefaultCvSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from job_posting import serializers as jobpost_serializers
from rest_framework.views import APIView
from django.core.serializers import serialize
import json
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination
# Create your views here.


class ApplicationView(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ApplicationSerializer
    queryset = Application.objects.all()
    pagination_class = LimitOffsetPagination

    @action(detail=False, methods=['get'], url_path="get_user_applications")
    def get_user_applications(self, request):
        try:
            user = request.user
            applications = Application.objects.filter(
                applicant=user.id).select_related("job_posting")
            if not applications:
                return Response({"message": "No applications found for current user",
                                 "data": []},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                data = []
                applications = self.paginate_queryset(applications)
                for application in applications:

                    application_data = serializers.ApplicationSerializerForJobListings(
                        application).data
                    application_data["job_posting"] = jobpost_serializers.JobPostSerializerForApplicationListing(
                        application.job_posting).data
                    data.append(application_data)
                return self.get_paginated_response(data)
                # return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(getattr(e, 'message', repr(e)))
            return Response({"message": "WHOOPS, and error occurred; " + getattr(e, 'message', repr(e))},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        application = self.get_object()
        application_data = self.get_serializer(application).data
        application_data["job_posting"] = jobpost_serializers.JobPostSerializer(
            application.job_posting).data
        return Response(application_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_status_options(self, request):
        status_options = Application.STATUSES
        status_options_2 = [
            {"value": option[0], "label": option[1]} for option in status_options]
        return Response(status_options_2, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path="search")
    def search_applications(self, request):
        print(request.data, file=sys.stderr)
        searchString = request.data['searchString']
        user = request.user
        searchTerms = searchString.split()
        applications = None
        for term in searchTerms:
            term_queryset = Application.objects.filter(
                Q(job_posting__title__icontains=term) | Q(job_posting__description__icontains=term)).filter(applicant=user.id)

            if applications == None:
                applications = term_queryset
            else:
                applications = applications | term_queryset

        if not applications:
            return Response({"message": "No applications found with the search term",
                             "data": []},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            data = []
            for application in applications:
                application_data = serializers.ApplicationSerializerForJobListings(
                    application).data
                application_data["job_posting"] = jobpost_serializers.JobPostSerializerForApplicationListing(
                    application.job_posting).data
                data.append(application_data)
            return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path="get_jobposting_application")
    def get_jobposting_application(self, request):
        try:
            jobpostingId = request.headers['posting']
            print(jobpostingId)
            applications = Application.objects.filter(
                job_posting=jobpostingId).select_related("job_posting")
            if not applications:
                return Response({"message": "No applications found for this job posting",
                                 "data": []},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                data = []
                user = {}
                cv = {}
                # applicant = [user, cv]
                applications = self.paginate_queryset(applications)
                for application in applications:
                    application_data = serializers.ApplicationSerializerForEmployer(
                        application).data
                    application_data["cv"] = DefaultCvSerializer(
                        application.cv).data
                    application_data["applicant"] = UserSerializer(
                        application.applicant).data
                    data.append(application_data)
                return self.get_paginated_response(data)
                # WITHOUT serializer
                # cv = CvBasic.objects.get(
                #     id=application.cv.id)  # should be application.applicant.id for single cv
                # user = UserAccount.objects.get(  # but the records in the database make that impossible
                #     id=application.applicant.id)
                # if (user == None or cv == None):
                #     continue
                # cv = CvSerializer(cv).data
                # user = UserSerializer(user).data

                # applicant[0] = cv
                # applicant[1] = user
                # data.append(applicant)

                # return Response(data, status=status.HTTP_200_OK, headers={"Access-Control-Allow-Origin": "*"})
        except Exception as e:
            print(getattr(e, 'message', repr(e)))
            return Response({"message": "WHOOPS, and error occurred; " + getattr(e, 'message', repr(e))},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class ApplicationSearchView(APIView):

#     def get(self, request):
#         print(request.user, file=sys.stderr)
#         searchString = request.body.searchString
#         user = request.user
#         searchTerms = searchString.split()
#         query = None
#         for t in searchTerms:
#             q = Application.objects.filter(
#                 Q(title__icontains=t) | Q(description__icontains=t)).filter(applicant=user.id)

#             if query == None:
#                 query = q
#             else:
#                 query = query | q

#         jsonquery = json.loads(serialize('json', query))

#         print(searchTerms, file=sys.stderr)
#         return Response(jsonquery, status=status.HTTP_200_OK)
