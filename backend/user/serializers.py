from rest_framework import serializers
from .models import User
from cv.serializers import *

class UserSerializer(serializers.ModelSerializer):
    cvs = DefaultCvSerializer(many=True)
    
    class Meta:
        model = User
        fields = '__all__'
        
class DefaultUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'