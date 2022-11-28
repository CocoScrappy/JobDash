from django.shortcuts import render
from rest_framework import viewsets,status,mixins
from . import serializers
from .models import JobPost
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class DefaultJobPostView(viewsets.ModelViewSet):
    serializer_class = serializers.DefaultJobPostSerializer
    queryset = JobPost.objects.all()
    

class JobPostView(viewsets.ModelViewSet):
    serializer_class = serializers.JobPostSerializer
    queryset = JobPost.objects.all()

class JobSearchView(APIView):
    # serializer_class = serializers.JobPostSerializer


    def get(self,request,par):
        searchTerms=par
        # query=self.request.GET.get('search')
        return Response(searchTerms,status=status.HTTP_200_OK)