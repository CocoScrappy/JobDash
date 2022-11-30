from rest_framework import serializers
from .models import *
# from application.serializers import DefaultApplicationSerializer


class DefaultJobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'


class JobPostSerializer(serializers.ModelSerializer):
    # applications = DefaultApplicationSerializer(many=True)

    class Meta:
        model = JobPost
        fields = '__all__'

class JobPostSerializerForApplicationListing(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = 'id', 'title', 'company', 'location', 'remote_option'