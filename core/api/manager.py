from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    '''manages User account creation'''

    def create_user(self, email, password, fname='-', lname='-', **kwargs):
        # method to create an ordinary user
        user = self.model(email=email, password=password,
                          fname=fname, lname=lname, **kwargs)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user

    def create_staff(self, email, password, fname='-', lname='-', **kwargs):
        # method to create a staff/admin user
        user = self.model(email=email, password=password,
                          fname=fname, lname='-', **kwargs)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = False
        user.save()
        return user

    def create_superuser(self, email, password, fname='-', lname='-', **kwargs):
        # method to create a superuser
        user = self.create_user(
            email,  password, fname='-', lname='-', **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
