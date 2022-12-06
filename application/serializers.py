from rest_framework import serializers
from .models import *
from cv.serializers import DefaultCvSerializer
from job_posting.serializers import JobPostSerializer


class SavedDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saved_Date
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    saved_dates = SavedDatesSerializer(many=True, allow_null=True)

    class Meta:
        model = Application
        fields = '__all__'


class ApplicationSerializerForJobListings(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'application_date', 'favorited', 'status')


class ApplicationWithDatesSerializer(serializers.ModelSerializer):
    saved_dates = SavedDatesSerializer(many=True)

    class Meta:
        model = Saved_Date
        fields = '__all__'


class ApplicationSerializerForEmployer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = 'id', 'cv', 'applicant'
