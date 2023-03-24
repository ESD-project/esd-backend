from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from entities.manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_fullname(self):
        '''return the full name of the user'''
        return self.fullname if self.fullname else self.email

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.fullname if self.fullname else self.email

    class Meta:
        db_table = 'user'
