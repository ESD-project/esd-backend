from django.shortcuts import render
from rest_framework.views import APIView
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import RegisterSerializer, UserSerializer


class OverViewEndpoint(APIView):
    def get(self, request):
        return Response({
            'message': 'Hello, world!'
        })


class LoginAPI(KnoxLoginView):
    '''Login api endpoint'''
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class RegisterStaffAPI(generics.GenericAPIView):
    '''This CBV is used to register a new staff user'''
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1],
        }, status=status.HTTP_201_CREATED)


class ChangePasswordAPI(APIView):
    '''This CBV is used to change a user's password'''
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        new_password = request.data.get('new_password')
        if new_password:
            user.set_password(new_password)
            user.save()
            return Response({
                "message": "Password Changed Successfully",
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Invalid Password Length!",
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPI(APIView):
    '''This CBV is used to get a user's profile'''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            "user": UserSerializer(user).data,
        }, status=status.HTTP_200_OK)
