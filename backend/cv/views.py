from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from .models import *

# Create your views here.
class CvsView(viewsets.ModelViewSet):
    serializer_class = serializers.CvSerializer
    queryset = CV.objects.all()
    
class DefaultCvsView(viewsets.ModelViewSet):
    serializer_class = serializers.DefaultCvSerializer
    queryset = CV.objects.all()
    
class CvElementsView(viewsets.ModelViewSet):
    serializer_class = serializers.CvElementSerializer
    queryset = CV_elements.objects.all()