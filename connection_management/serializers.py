from rest_framework.serializers import ModelSerializer
from .models import *
from user_management.models import Uuser



class User_Serializer(ModelSerializer):
    class Meta:
        model = Uuser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'profile_image', 'rating', 'is_artisan','is_active', 'is_superuser', 'about']

class Connections_Serializer(ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'
        
class Connected_Users_Serializer(ModelSerializer):
    from_users= User_Serializer(source='from_user', read_only=True)
    to_users = User_Serializer(source='to_user', read_only=True)
    class Meta:
        model = Connection
        fields = ['id','from_users', 'to_users', 'status', 'created_at'] 
            