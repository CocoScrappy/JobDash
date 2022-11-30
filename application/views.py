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
from job_posting.serializers import JobPostSerializer

# Create your views here.


class ApplicationView(viewsets.ModelViewSet):
    # permission_classes=[permissions.IsAuthenticated]
    serializer_class = serializers.ApplicationSerializer
    queryset = Application.objects.all()

    @action(detail=False, methods=['get'], url_path="get_user_applications")
    def get_user_applications(self, request):
        try:
            user = request.user
            print(user)
            applications = Application.objects.filter(
                applicant=user.id).select_related("job_posting")
            if not applications:
                return Response({"message": "No applications found for current user",
                                 "data": []},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                data = []
                for application in applications:
                    job_posting_data = JobPostSerializer(
                        application.job_posting).data
                    job_posting_data['application'] = self.get_serializer(
                        application).data
                    data.append(job_posting_data)
                print(data)
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(getattr(e, 'message', repr(e)))
            return Response({"message": "WHOOPS, and error occurred; " + getattr(e, 'message', repr(e))},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path="get_jobposting_application")
    def get_user_applications(self, request):
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


# class DefaultApplicationView(viewsets.ModelViewSet):
#     serializer_class = serializers.DefaultApplicationSerializer
#     queryset = Application.objects.all()
