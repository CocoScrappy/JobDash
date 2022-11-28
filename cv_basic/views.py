from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from . import serializers
from .models import *
from user.models import UserAccount
from django.shortcuts import get_object_or_404
from django import http
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.


class CvsView(viewsets.ModelViewSet):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = serializers.DefaultCvSerializer
    queryset = CvBasic.objects.all()
    
    def create(self, request):
        try:
            user = request.user
            print(user)
            cv = request.data
            print(cv)
            cv["user"] = user.id
            print(cv)
            serializer = self.get_serializer(data=cv)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            
        except CvBasic.DoesNotExist:
            return Response({"message": "Cannot find a CV for the requested user"},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path="get_user_cvs")
    def get_user_cvs(self, request):
        # JWT_authenticator = JWTAuthentication()
        # response = JWT_authenticator.authenticate(request)
        # if response is not None:
        #     # unpacking
        #     user , token = response
        #     print("this is decoded token claims", token.payload)
        #     print("user associated with this token is", user)
        #     print("userId = ", user.id)
        # else:
        #     print("no token is provided in the header or the header is missing")
        try:
            user = request.user;
            cvs = CvBasic.objects.get(user=user.id)
            cvs_serializer = serializers.DefaultCvSerializer(cvs)
            return Response(cvs_serializer.data, status=status.HTTP_200_OK)
        except CvBasic.DoesNotExist:
            return Response({"message": "Cannot find a CV for the requested user"},
                            status=status.HTTP_400_BAD_REQUEST)

        # cvs=serializers.DefaultCvSerializer("json", list(cvs), many=True)
        # print(cvs)

