from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from . import serializers
from rest_framework.decorators import action
from .models import JobPost
from rest_framework.response import Response

# Create your views here.


class DefaultJobPostView(viewsets.ModelViewSet):
    serializer_class = serializers.DefaultJobPostSerializer
    queryset = JobPost.objects.all()


class JobPostView(viewsets.ModelViewSet):
    serializer_class = serializers.JobPostSerializer
    queryset = JobPost.objects.all()

    @action(detail=False, methods=['get'], url_path="get_user_postings")
    def get_user_job_postings(self, request):
        try:
            user = request.user

            userPosts = JobPost.objects.filter(
                employer=user.id).select_related("employer")

            if not userPosts:
                return Response({"message": "No job postings found for current user",
                                 "data": []},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                data = []
                for post in userPosts:
                    posting = self.get_serializer(post).data
                    data.append(posting)
                # print(data)
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(getattr(e, 'message', repr(e)))
            return Response({"message": "WHOOPS, and error occurred; " + getattr(e, 'message', repr(e))},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
