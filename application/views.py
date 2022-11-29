from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from . import serializers
from .models import Application
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
class ApplicationView(viewsets.ModelViewSet):
    # permission_classes=[permissions.IsAuthenticated]
    serializer_class = serializers.ApplicationSerializer
    queryset = Application.objects.all()
    
    @action(detail=False, methods=['get'], url_path="get_user_applications")
    def get_user_applications(self, request):
        try:
            user = request.user;
            print(user)
            applications = Application.objects.filter(applicant=user.id).values()
            print(applications)
            if not applications:
                return Response({"message": "No applications found for current user",
                                 "data": []},
                            status=status.HTTP_404_NOT_FOUND)
            else:
                # application_serializer = serializers.ApplicationSerializer(applications)
                # application_serializer = serializers.(applications)
                return Response(applications, status=status.HTTP_200_OK)
        except Exception as e:
            print(getattr(e, 'message', repr(e)))
            return Response({"message": "WHOOPS, and error occurred"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class DefaultApplicationView(viewsets.ModelViewSet):
    serializer_class = serializers.DefaultApplicationSerializer
    queryset = Application.objects.all()
    