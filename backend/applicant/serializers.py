from rest_framework import serializers
from .models import Applicant

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ('id', 'first_name', 'last_name', 'email', 'summary', 'password', 'role')