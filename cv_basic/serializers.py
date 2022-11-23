from rest_framework import serializers
from .models import *
from application.serializers import DefaultApplicationSerializer

      
class DefaultCvSerializer(serializers.ModelSerializer):
    class Meta:
        model = CvBasic
        fields = '__all__'

class CvSerializer(serializers.ModelSerializer):
    applications = DefaultApplicationSerializer(many=True)
    
    class Meta:
        model = CvBasic
        fields = '__all__'
