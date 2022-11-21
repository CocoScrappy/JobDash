from rest_framework import serializers
from .models import *
from cv.serializers import DefaultCvSerializer
from job_posting.serializers import DefaultPostingSerializer

        
class ApplicationSerializer(serializers.ModelSerializer):
    cv = DefaultCvSerializer(many=True)
    # job_posting = DefaultJobPostingSerializer(many=True)
    
    class Meta:
        model = Application
        fields = '__all__'
        
class DefaultApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
