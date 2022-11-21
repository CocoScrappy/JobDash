from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from .models import JobPost

# Create your views here.
class PostingView(viewsets.ModelViewSet):
    serializer_class = serializers.PostingSerializer
    queryset = JobPost.objects.all()
    
    