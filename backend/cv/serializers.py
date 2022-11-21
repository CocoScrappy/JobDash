from rest_framework import serializers
from .models import *
from user import serializers as user_serializers


class CvElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV_elements
        fields = '__all__'
        
class CvSerializer(serializers.ModelSerializer):
    cv_elements = CvElementSerializer(many=True)
    
    class Meta:
        model = CV
        fields = '__all__'
        
class DefaultCvSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = '__all__'
