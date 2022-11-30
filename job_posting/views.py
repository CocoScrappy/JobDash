import sys
from django.shortcuts import render
from rest_framework import viewsets,status,mixins
from . import serializers
from .models import JobPost
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.serializers import serialize
import json
from django.db.models import Q

# Create your views here.
class DefaultJobPostView(viewsets.ModelViewSet):
    serializer_class = serializers.DefaultJobPostSerializer
    queryset = JobPost.objects.all()
    

class JobPostView(viewsets.ModelViewSet):
    serializer_class = serializers.JobPostSerializer
    queryset = JobPost.objects.all()

class JobSearchView(APIView):
    serializer_class = serializers.JobPostSerializer


    def get(self,request,par):
        
        searchTerms=par.split()
        query=None
        for t in searchTerms:
            q=JobPost.objects.filter(Q(title__icontains=t)|Q(description__icontains=t))
            
            if query==None:
                query=q
            else:
                query=query|q
        
        jsonquery=json.loads(serialize('json',query))
        

        print(searchTerms, file=sys.stderr)
        return Response(jsonquery,status=status.HTTP_200_OK)