
"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,PermissionsMixin,BaseUserManager
)

# Create your models here.



class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email :
            raise ValueError("The email feild is null or not filled")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,password):
        user = self.create_user(email=email,password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Accounts(models.Model):
    """Accouts model fields"""
    pcode = models.IntegerField()  # Field name made lowercase.
    extension = models.CharField(unique=True, max_length=4)
    secret = models.CharField(max_length=20)
    callerid = models.CharField(max_length=100)
    mailbox = models.EmailField(max_length=50)
    zones = models.CharField(max_length=100,null=True,blank=True)
    level = models.CharField(max_length=50)
    groups = models.CharField(max_length=80, blank=True, null=True)  # Field name made lowercase.
    cfwd = models.CharField(max_length=30, blank=True, null=True)  # Field name made lowercase.
    regione = models.CharField( max_length=25, blank=True, null=True)  # Field name made lowercase.
    server = models.CharField(max_length=50)  # Field name made lowercase.
    enable = models.IntegerField(db_column='Enable')# Field name made lowercase.
    lastupdate = models.DateField(db_column='LastUpdate',auto_now=True,blank=True, null=True)

    def __str__(self) -> str:
        return self.extension