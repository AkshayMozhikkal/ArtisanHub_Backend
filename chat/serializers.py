from rest_framework.serializers import ModelSerializer
from .models import Message
from user_management.models import *
from rest_framework import serializers

class UserListserializer(ModelSerializer):
   class Meta:
        model = Uuser
        fields = ['id', 'email', 'first_name','last_name', 'profile_image']

class MessageSerializer(ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email')

    class Meta:
        model = Message
        fields = ['message', 'sender_email']

class ChatSerializer(ModelSerializer):
     class Meta:
         model = Message
         fields ='__all__'        