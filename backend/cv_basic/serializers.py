from rest_framework import serializers
from .models import *
from user import serializers as user_serializers

      
class DefaultCvSerializer(serializers.ModelSerializer):
    class Meta:
        model = CvBasic
        fields = '__all__'
