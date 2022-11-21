from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from .models import User

# Create your views here.
class Default_Users_View(viewsets.ModelViewSet):
    serializer_class = serializers.DefaultUserSerializer
    queryset = User.objects.all()
    
class Users_With_CV_View(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()