from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from .models import JobPost

# Create your views here.
class DefaultJobPostView(viewsets.ModelViewSet):
    serializer_class = serializers.DefaultJobPostSerializer
    queryset = JobPost.objects.all()
    

class JobPostView(viewsets.ModelViewSet):
    serializer_class = serializers.JobPostSerializer
    queryset = JobPost.objects.all()
