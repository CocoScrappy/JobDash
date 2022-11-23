from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from .models import Application

# Create your views here.
class ApplicationView(viewsets.ModelViewSet):
    serializer_class = serializers.DefaultApplicationSerializer
    queryset = Application.objects.all()
    
class DefaultApplicationView(viewsets.ModelViewSet):
    serializer_class = serializers.DefaultApplicationSerializer
    queryset = Application.objects.all()
    