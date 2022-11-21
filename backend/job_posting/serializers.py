from rest_framework import serializers
from .models import *
from user.serializers import DefaultUserSerializer
 
class PostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        
