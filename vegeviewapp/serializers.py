from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
import re

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    middle_name = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('prefer-not-to-say', 'Prefer not to say')])
    date_of_birth = serializers.DateField()
    organization = serializers.CharField(required=True, allow_blank=False)
    job_title = serializers.CharField(required=True, allow_blank=False)
    data_use = serializers.ChoiceField(choices=[('research', 'Research'), ('business-analysis', 'Business Analysis'), ('education', 'Education'), ('personal-use', 'Personal Use'), ('other', 'Other')])
    additional_details = serializers.CharField(required=True, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'middle_name', 'last_name', 'password', 'confirm_password', 'gender', 'date_of_birth', 'organization', 'job_title', 'data_use', 'additional_details']

    def validate_username(self, value):
        if len(value) < 3 or len(value) > 150:
            raise serializers.ValidationError('The username must be between 3 and 150 characters.')
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError('The username can only contain alphanumeric characters and underscores.')
        return value

    def validate_email(self, value):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
            raise serializers.ValidationError('The email is not a valid email address.')
        return value
    
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})

        if len(password) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long"})
        if not re.search("[a-z]", password):
            raise serializers.ValidationError({"password": "Password must contain at least one lowercase letter"})
        if not re.search("[A-Z]", password):
            raise serializers.ValidationError({"password": "Password must contain at least one uppercase letter"})
        if not re.search("[0-9]", password):
            raise serializers.ValidationError({"password": "Password must contain at least one digit"})
        if not re.search("[`~@#$%^&*()_+=]", password):
            raise serializers.ValidationError({"password": "Password must contain at least one special character"})
        if password == data.get('username'):
            raise serializers.ValidationError({"password": "Password cannot be the same as username"})
       
        return data

 
    def create(self, validated_data):
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        # Create UserProfile instance
        UserProfile.objects.create(
            user=user,
            middle_name=validated_data.get('middle_name', ''),
            gender=validated_data.get('gender'),
            date_of_birth=validated_data.get('date_of_birth'),
            organization=validated_data.get('organization', ''),
            job_title=validated_data.get('job_title', ''),
            data_use=validated_data.get('data_use', ''),
            additional_details=validated_data.get('additional_details', '')
        )

        return user
