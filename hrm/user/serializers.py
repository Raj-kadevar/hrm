from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from virtualenv.app_data import read_only

from .models import User, LeaveStatus, Device


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'profile', 'email', 'password' ,'password2']
        read_only_fields = ('is_active', )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['email']
            )
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        attrs.pop('password2')
        return attrs

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LeaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveStatus
        fields = ['leave_type', 'leave_start_date', 'leave_end_date']


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class AuthSerializer(serializers.Serializer):
    '''serializer for the user authentication object'''
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if not user:
            msg = ('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
