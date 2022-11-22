from rest_framework import serializers
from .models import User
from cv.serializers import *
from job_posting.serializers import *
from application.serializers import *

class UserSerializer(serializers.ModelSerializer):
    cvs = CvSerializer(many=True)
    postings = PostingSerializer(many=True)
    applications = DefaultApplicationSerializer(many=True)
    
    class Meta:
        model = User
        fields = '__all__'
        depth = 2
        
class DefaultUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'