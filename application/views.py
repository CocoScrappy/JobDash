from django.shortcuts import render
from rest_framework import viewsets, status, permissions

from user.models import UserAccount
from user.serializers import UserSerializer
from . import serializers
from .models import Application
from cv_basic.models import CvBasic
from cv_basic.serializers import CvSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from job_posting import serializers as jobpost_serializers

# Create your views here.


class ApplicationView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ApplicationSerializer
    queryset = Application.objects.all()

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
                for application in applications:
                    application_data = serializers.ApplicationSerializerForJobListings(
                        application).data
                    application_data["job_posting"] = jobpost_serializers.JobPostSerializerForApplicationListing(
                        application.job_posting).data
                    data.append(application_data)
                return Response(data, status=status.HTTP_200_OK)
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

    @action(detail=False, methods=['get'], url_path="get_jobposting_application")
    def get_jobposting_application(self, request):
        try:
            jobpostingId = request.headers['posting']
            print(jobpostingId)
            applications = Application.objects.filter(
                job_posting=jobpostingId).select_related("job_posting")
            if not applications:
                return Response({"message": "No applications found for current user",
                                 "data": []},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                data = []
                users = []
                cvs = []
                for application in applications:
                    cv = CvBasic.objects.get(
                        id=application.applicant.id)
                    cv = CvSerializer(cv).data
                    cvs.append(cv)
                    user = UserAccount.objects.get(
                        id=application.applicant.id)
                    user = UserSerializer(user).data
                    users.append(user)
                data.append(users)
                data.append(cvs)
                return Response(data, status=status.HTTP_200_OK, headers={"Access-Control-Allow-Origin": "*"})
        except Exception as e:
            print(getattr(e, 'message', repr(e)))
            return Response({"message": "WHOOPS, and error occurred; " + getattr(e, 'message', repr(e))},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(application_data, status=status.HTTP_200_OK)
