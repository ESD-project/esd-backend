from django.contrib.auth import authenticate
from entities.models import User
from rest_framework import serializers
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return Response(user, status=200)
        raise Response(
            {"error": "Unable to log in with provided credentials."}, status=400)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('fname', 'lname', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            fname=validated_data['fname'],
            lname=validated_data['lname'],
        )
        return user
