from api.models import Car
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
            'title': 'Hello, world!',
            'message': 'API IS WORKING!',
        })


class LoginAPI(KnoxLoginView):
    '''Login api endpoint'''
    permission_classes = [permissions.AllowAny]

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


class RegisterUserAPI(generics.GenericAPIView):
    '''This CBV is used to register a new ordinary user'''
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


class CarListAPI(APIView):
    '''This CBV is used to get the list of all cars in the system'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        cars = Car.objects.all().order_by('id')
        return Response({
            "cars": CarSerializer(cars, many=True).data,
        }, status=status.HTTP_200_OK)


class CarDetailAPI(APIView):
    '''This CBV is used to get the details of a car'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        car_id = request.data.get('car_id')
        car = Car.objects.filter(id=car_id).first()
        return Response({
            "car": CarSerializer(car, many=False).data,
        }, status=status.HTTP_200_OK)


class DeleteCarAPI(APIView):
    '''This CBV is used to delete a car'''
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        car_id = request.data.get('car_id')
        car = Car.objects.filter(id=car_id).first()
        if car:
            car.delete()
            return Response({
                "message": "Car Deleted Successfully",
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Car Not Found",
            }, status=status.HTTP_404_NOT_FOUND)


class RentalListAPI(APIView):
    '''This CBV is used to get the list of all rentals in the system'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        rentals = Rental.objects.all().order_by('id')
        return Response({
            "rentals": RentalSerializer(cars, many=True).data,
        }, status=status.HTTP_200_OK)


class RentalDetailAPI(APIView):
    '''This CBV is used to get the details of a rental'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        rental_id = request.data.get('rental_id')
        rental = Rental.objects.filter(id=rental_id).first()
        return Response({
            "rental": RentalSerializer(rental, many=False).data,
        }, status=status.HTTP_200_OK)


class RentalSlotListAPI(APIView):
    '''This CBV is used to get the list of all rental slots'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        rentalslots = RentalSlot.objects.all().order_by('id')
        return Response({
            "rentalslots": RentalSlotsSerializer(rentalslots, many=True).data,
        }, status=status.HTTP_200_OK)


class RentalSlotDetailAPI(APIView):
    '''This CBV is used to get the details of a rental slot'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        rental_slot_id = request.data.get('rental_slot_id')
        rentalslot = RentalSlot.objects.filter(id=rental_slot_id).first()
        return Response({
            "rentalslot": RentalSlotsSerializer(rentalslot, many=False).data,
        }, status=status.HTTP_200_OK)
