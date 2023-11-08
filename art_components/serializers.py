from rest_framework.serializers import ModelSerializer, Serializer
from .models import  *



class Banner_Serializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'