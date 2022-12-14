from email.policy import default
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=255)
    #user_key = models.CharField(max_length=50, default="" ,blank=None, null=True)
    user_nickname = models.CharField(max_length=50, default="" ,blank=True)
    user_name=models.CharField(max_length=50, default="" ,blank=True)
    user_mbti=models.CharField(max_length=50, default="" ,blank=True)
    user_keyword1=models.CharField(max_length=50, default="" ,blank=True)
    user_keyword2=models.CharField(max_length=50, default="" ,blank=True)
    user_keyword3=models.CharField(max_length=50, default="" ,blank=True)
    #user_email=models.CharField(max_length=50, default="" ,blank=None, null=True)
    user_status=models.CharField(max_length=50, default="0" ,blank=True)
    #user_register_dttm= models.DateField(auto_now_add=True)
    user_profile_img=models.ImageField(upload_to='%Y%m%d/' ,blank=True,default='')
    user_auth_email=models.CharField(max_length=50, default="" ,blank=True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email