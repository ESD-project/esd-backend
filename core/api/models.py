from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from api.manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    dob = models.DateField(blank=True, null=True)
    id_type = models.CharField(max_length=50, blank=True, null=True)
    id_number = models.CharField(max_length=50, blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    proof_of_id = models.ImageField(upload_to='proof_of_id', blank=True, null=True)  # noqa
    residential_address = models.CharField(max_length=250, blank=True, null=True)  # noqa
    telephone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_fullname(self):
        '''return the full name of the user'''
        return self.fname + ' ' + self.lname

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.fullname if self.fullname else self.email

    class Meta:
        db_table = 'user'


class Brand(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'brand'


class Car(models.Model):
    image = models.ImageField(upload_to='car_images')
    model = models.CharField(max_length=100)
    colour = models.CharField(max_length=100)
    seats = models.IntegerField()
    car_type = models.CharField(max_length=100)
    number_plate = models.CharField(max_length=50)

    brand = models.OneToOneField(Brand, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.model

    class Meta:
        db_table = 'car'


class RentalSlot(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.car.model

    class Meta:
        db_table = 'rental_slot'


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rental_slot = models.ForeignKey(RentalSlot, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_cost(self):
        '''return the total cost of the rental'''
        return self.rental_slot.price_per_day * (self.end_date - self.start_date).days

    def __str__(self):
        return self.user.fname if self.user.fname else self.user.email

    class Meta:
        db_table = 'rental'
