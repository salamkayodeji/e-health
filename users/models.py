from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _



class UserProfileManager(BaseUserManager):
    """ Manager for user profiles """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self._create_user(email, password, **extra_fields)
    

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Database model for users in the system """
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length = 100)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone', 'category']
    
    def get_full_name(self):
        return self.full_name

PARTICULARS = (
('Malaria', 'Malaria'),
('Typhoid', 'Typhoid'),
('Ebola', 'Ebola'),
('Diabetes ', 'Diabetes')
)

GENDER = (
('MALE', 'MALE'),
('FEMALE', 'FEMALE'),
)

class Medical_History(models.Model):
    email = models.OneToOneField(UserProfile,on_delete = models.CASCADE)
    gender = models.CharField(max_length=30, choices=GENDER)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True)
    age = models.IntegerField(default= 0 )
    blood = models.CharField(max_length=10, blank=True)
    ailment = models.CharField(max_length=100, choices=PARTICULARS)
    
    def __str__(self):
        return str(self.email)

