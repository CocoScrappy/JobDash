from rest_framework import serializers
from .models import *
from cv.serializers import DefaultCvSerializer
from job_posting.serializers import JobPostSerializer

        
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        
class ApplicationSerializerForJobListings(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('application_date', 'favorited', 'status')
