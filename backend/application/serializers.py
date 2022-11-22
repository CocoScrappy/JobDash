from rest_framework import serializers
from .models import *
from cv_basic.serializers import DefaultCvSerializer
from job_posting.serializers import PostingSerializer

        
class ApplicationSerializer(serializers.ModelSerializer):
    cv = DefaultCvSerializer(many=True)
    job_posting = PostingSerializer(many=True)
    
    class Meta:
        model = Application
        fields = '__all__'
        
class DefaultApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
