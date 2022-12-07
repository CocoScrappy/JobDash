from django.shortcuts import render
from rest_framework import viewsets, status, permissions
import sys
from user.serializers import UserSerializer
from . import serializers
from .models import Application, Saved_Date
from cv_basic.serializers import DefaultCvSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from job_posting import serializers as jobpost_serializers
from django.core.serializers import serialize
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination
from job_posting.models import JobPost


class ApplicationView(viewsets.ModelViewSet):
    """

    *Context*

    **def create(self, request, *args, **kwargs):**

        url = /api/applications/

        method = post

        Creates a new applications to a particular job posting.

        The request body should include at least the required information in the :model:`application.Application` model, except for the applicant id which is extracted from the header's authorization token.

        The method validates that the user did not apply for the same job posting before. If applying to same application twice, it will return an HTTP_403_FORBIDDEN response with an error message.


    **def get_user_applications(self, request):**

        url = /api/applications/get_user_applications/

        method = get

        gets the list of applications of the logged in user.

        The method gets the user from the request header's token, then perform a query to the database to get the applications with applicant as the logged in user.

        Returns a response with array of applications including necessary information for listing applications (id, job title, company, application date, remote option, favorited).

        if no application found for the current user, it will return a response with an empty array.


    **def details(self, request, pk=None):**

        url = /api/applications/{pk}/details/

        method = get

        gets all the information associated with a job application (:model:`application.Application`), including job post (:model:`job_posting.JobPost`) and saved dates (:model:`application.Saved_Date`).

        The method gets the user from the request header's token, then perform a a validation to check if the logged in user is authorized to get the application details (they should be the applicant).

        Returns a response with JSON object conatining the application details.

        If user requesting is not the application's aplicant, ir will return an error message with HTTP_401_UNAUTHORIZED status.



    **def get_status_options(self, request):**

        url = /api/applications/get_status_options

        method = get

        gets the job application status options from :model:`application.Application`.


    **def search_applications(self, request):**

        url = /api/applications/search_applications

        method = get

        Allows to search for the list of user's application, related to :model:`application.Application`, returns a serialized queryset with all the matches.

        Gets the search string from the request body and the user id from the request user (token)


    **def get_jobposting_application(self, request):**

        url = /api/applications/get_jobposting_application/

        method = get

        Returns a paginated and serialized queryset for each applications to a particular job posting.

        For each application the query composes an object made of application id, cv model and user model.

        The employer id in job posting is verified against the request user id from the token.

    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ApplicationSerializer
    queryset = Application.objects.all()
    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            request.data['applicant'] = user.id
            # if request.data['applicant'] != user:
            #     return Response({'message': "You cannot aply using other user's information"}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = self.get_serializer(data=request.data)
            print(request.data)
            serializer.is_valid(raise_exception=True)
            application_data = serializer.validated_data
            job_posting_applications = Application.objects.filter(
                job_posting=application_data['job_posting']).filter(applicant=user)
            print(job_posting_applications)
            if len(job_posting_applications) > 0:
                return Response({'message': 'You already applied to this job posting'}, status=status.HTTP_403_FORBIDDEN)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print(getattr(e, 'message', repr(e)))
            return Response({"message": getattr(e, 'message', repr(e))},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path="get_user_applications")
    def get_user_applications(self, request):
        """
        gets the list of applications of the logged in user.

        The method gets the user from the request header's token, then perform a query to the database to get the applications with applicant as the logged in user.

        Returns a response with array of applications including necessary information for listing applications (id, job title, company, application date, remote option, favorited).

        if no application found for the current user, it will return a response with an empty array.

        """
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
        """
        gets all the information associated with a job application (:model:`application.Application`), including job post (:model:`job_posting.JobPost`) and saved dates (:model:`application.Saved_Date`).

        The method gets the user from the request header's token, then perform a a validation to check if the logged in user is authorized to get the application details (they should be the applicant).

        Returns a response with JSON object conatining the application details.

        If user requesting is not the application's aplicant, ir will return an error message with HTTP_401_UNAUTHORIZED status.

        """
        user = request.user
        application = self.get_object()
        if application.applicant != user:
            return Response({"message": "You are unauthorized to view this application"}, status=status.HTTP_401_UNAUTHORIZED)
        application_data = self.get_serializer(application).data
        application_data["job_posting"] = jobpost_serializers.JobPostSerializer(
            application.job_posting).data
        application_data["saved_dates"] = serializers.SavedDatesSerializer(
            application.saved_dates, many=True).data
        return Response(application_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_status_options(self, request):
        """
        gets the job application status options from :model:`application.Application`.

        """
        status_options = Application.STATUSES
        status_options_2 = [
            {"value": option[0], "label": option[1]} for option in status_options]
        return Response(status_options_2, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path="search")
    def search_applications(self, request):
        """

        Allows to search for the list of user's application, related to :model:`application.Application`, returns a serialized queryset with all the matches.

        gets the search string from the request body and the user id from the request user (token)

        """
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
        """
        Returns a paginated and serialized queryset for each applications to a particular job posting.
        For each application the query composes an object made of application id, cv model and user model.

        The employer id in job posting is verified against the request user id from the token.

        **Context**

        ``jobpostingId = request.headers['posting']``
        headers are used to transfer job posting id to the backend

        """
        try:

            jobpostingId = request.headers['posting']
            jobposting = JobPost.objects.get(pk=jobpostingId)
            user = request.user

            if jobposting.employer != user:
                return Response({"message": "You are unauthorized to view these applications"}, status=status.HTTP_401_UNAUTHORIZED)
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


class SavedDatesView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.SavedDatesSerializer
    queryset = Saved_Date.objects.all()
    paginator = None
