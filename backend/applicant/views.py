from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ApplicantSerializer
from .models import Applicant

# Create your views here.
class List_Applicants_View(viewsets.ModelViewSet):
    serializer_class = ApplicantSerializer
    queryset = Applicant.objects.all()