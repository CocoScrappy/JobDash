from rest_framework import serializers
from .models import *
 
class PostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'
        
