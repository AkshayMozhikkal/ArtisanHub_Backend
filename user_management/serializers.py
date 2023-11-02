from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from .models import  Uuser , Address
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from work_management.models import *
from connection_management.models import *


class UuserSerializer(ModelSerializer):
    class Meta:
        model = Uuser
        fields = ['id', 'username', 'art', 'first_name', 'last_name', 'email', 'phone', 'profile_image', 'rating', 'is_artisan','is_active','is_superuser', 'password', 'about','date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
class EditUserSerializer(ModelSerializer):
    class Meta:
        model= Uuser
        fields = ['id','art' ,'first_name', 'last_name', 'email', 'phone', 'is_active', 'about', 'is_artisan']
                
# Token
class myTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        
        token = super().get_token(user)

        token['id']=user.id
        token['first_name']=user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['username'] = user.username
        token['is_artisan'] = user.is_artisan
        token['is_active'] = user.is_active
        token['is_admin'] = user.is_superuser
        token['phone'] = user.phone
        token['rating'] = user.rating

        return token        

class Upload_imageSerializer(ModelSerializer):
    class Meta:
        model = Uuser
        fields = ['profile_image']
        
class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'home','city', 'district', 'state', 'pin'] 
        
class UserWithAddressSerializer(ModelSerializer):
    user_info = UuserSerializer(source='user', read_only=True) 
    class Meta:
        model = Address
        fields = ['id', 'user_info', 'home', 'city', 'district', 'state', 'pin']
                
# User Google Account
class GoogleAuthSerializer(ModelSerializer):
    class Meta:
        model = Uuser 
        fields = ['id', 'username','art', 'first_name', 'last_name', 'email', 'phone', 'profile_image', 'rating', 'is_artisan','is_google']
        extra_kwargs = {
            'password': { 'write_only': True }
        }  


class Work_Serializer(ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'
        
class Connection_Serializer(ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'
        
         
class UserAllDataSerializer(ModelSerializer):
    works = Work_Serializer(many=True, read_only=True, source='user_works')
    address = AddressSerializer(read_only=True)
    connections = Connection_Serializer(many=True, read_only= True, source = 'user_connections')
    class Meta:
        model = Uuser
        fields = '__all__'              
                
class Location_Serializer (ModelSerializer):
     class  Meta:
         model = Address
         fields = ['city']     
         
         
class PasswordResetSerializer(Serializer):
    email = serializers.EmailField()         