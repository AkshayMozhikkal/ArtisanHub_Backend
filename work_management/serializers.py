from rest_framework import serializers
from user_management.models import Uuser
from .models import *


class UUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uuser
        fields = ['id','username', 'first_name', 'last_name', 'profile_image']
            
class Comment_Serializer(serializers.ModelSerializer):
    commented_by = UUserSerializer()
    class Meta:
        model = Comment
        fields = '__all__'  
        ordering = ['-commented_at']
        
class New_Comment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'   

class New_Like_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'   
        
class LikeSerializer(serializers.ModelSerializer):
    liked_by = UUserSerializer()
    class Meta:
        model = Like
        fields = '__all__'         
 
 
class Work_Serializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    artist = UUserSerializer(read_only=True,source='user')
    comments = Comment_Serializer(many=True, read_only=True, source='comment_set')
    likes = LikeSerializer(many=True, read_only=True, source='like_set')

    class Meta:
        model = Work
        fields = '__all__'

    def get_like_count(self, obj):
        return obj.get_like_count()

    def get_comment_count(self, obj):
        return obj.get_comment_count()
    
                
        
    