from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import get_user_model
from cv_basic.serializers import DefaultCvSerializer
User=get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('first_name','last_name','email','password','summary','role','id')
    
    def validate(self,data):
        user=User(**data)
        password=data.get('password')
        try:
            validate_password(password,user)
        except exceptions.ValidationError as e:
             serializer_errors=serializers.as_serializer_error(e)
             raise exceptions.ValidationError(
                {'password':serializer_errors['non_field_errors']}
             )
        return data

    
    def create(self,validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            summary=validated_data['summary'],
            role=validated_data['role']
        )
        
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','first_name','last_name','email','summary','role', 'password',)
        
    def create(self,validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            summary=validated_data['summary'],
            role=validated_data['role']
        )
        
        return user
    
class UserWithCVSerializer(serializers.ModelSerializer):
    cv = DefaultCvSerializer(many=False)
    class Meta:
        model=User
        fields=('id','first_name','last_name','email','summary','role', 'password',)
