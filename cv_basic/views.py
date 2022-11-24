from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from . import serializers
from .models import *
from user.models import UserAccount

# Create your views here.
class CvsView(viewsets.ModelViewSet):
    serializer_class = serializers.DefaultCvSerializer
    queryset = CvBasic.objects.all()
    
    @action(detail=False, methods=['get'], url_path="get_user_cvs")
    def get_user_cvs(self, request):
        email = request.headers.get("email")
        user = UserAccount.objects.get(email=email)
        cvs = CvBasic.objects.filter(user=user).values()

        # cvs=serializers.DefaultCvSerializer("json", list(cvs), many=True)
        # print(cvs)
        
        return Response(cvs, status=status.HTTP_200_OK)
    
    