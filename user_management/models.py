from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator





class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        

        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(email, password, **extra_fields)



# Create your models here.

class Uuser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    phone = models.BigIntegerField(blank=True, null=True)
    is_artisan = models.BooleanField(default=False)
    art = models.CharField(max_length=50, blank=True,null=True)
    rating = models.FloatField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_image', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_google = models.BooleanField(default=False)
    about = models.TextField(blank=True, null=True)
    field = models.CharField(max_length=60, null=True, blank=True)
    
     
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects=CustomUserManager()
    
    
class Address(models.Model):
    user = models.OneToOneField(Uuser, on_delete=models.CASCADE, blank=True, null=True)
    home = models.CharField(max_length=100)   
    city = models.CharField(max_length=100, null=True, blank=True) 
    district = models.CharField(max_length=150, blank=True, null=True)  
    state = models.CharField(max_length=150, blank=True, null=True)  
    pin = models.IntegerField(blank=True, null=True, validators=[
            MinValueValidator(limit_value=100000, message='PiN should have 6 numbers'),
            MaxValueValidator(limit_value=999999, message='PIN should have only 6 numbers'),
        ])  
    

    
  
    
    