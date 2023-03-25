from .models import RentalSlot
from .models import Rental
from .models import Car
from .models import Brand
from django.contrib.auth import authenticate
from api.models import User
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


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = "__all__"


class RentalSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalSlot
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"
