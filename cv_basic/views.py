from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from .models import *

# Create your views here.
class CvsView(viewsets.ModelViewSet):
    serializer_class = serializers.DefaultCvSerializer
    queryset = CvBasic.objects.all()
