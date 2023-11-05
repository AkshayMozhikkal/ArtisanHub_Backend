from django.shortcuts import render
from rest_framework.generics import *
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q


# Create your views here.

class Work_Posts(ListAPIView):
        queryset = Work.objects.all().order_by("-id")
        serializer_class = Work_Serializer
        
    
class New_Work(ListCreateAPIView):
    queryset =  Work.objects.all() 
    serializer_class = Work_Serializer  
    
class Single_Work(RetrieveUpdateDestroyAPIView):
        queryset = Work.objects.all()
        lookup_field = 'id'
        serializer_class = Work_Serializer   
        

class My_Works(ListAPIView):
        serializer_class = Work_Serializer  

        def get_queryset(self):
                user_id = self.kwargs['id']
                works = Work.objects.filter(user_id=user_id)
                return works

        def list(self, request, *args, **kwargs):
                queryset = self.get_queryset()
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
                
class Delete_Work(DestroyAPIView):
        lookup_field = 'id'
        queryset = Work.objects.all() 
        serializer_class =Work_Serializer       
        
        
class New_Comment(ListCreateAPIView):
    queryset =  Comment.objects.all() 
    serializer_class = New_Comment_Serializer                 
    
class Delete_Comment(DestroyAPIView):
    lookup_field='id'
    queryset =  Comment.objects.all() 
    serializer_class = New_Comment_Serializer  
    
class New_Like(ListCreateAPIView):  
        queryset = Like.objects.all()
        serializer_class = New_Like_Serializer

class Remove_Like(DestroyAPIView):
     def destroy(self, request, *args, **kwargs):
        user_id = request.data.get('liked_by')
        post_id = request.data.get('post')
        
        try:
            like = Like.objects.get(post_id=post_id, liked_by_id = user_id)
            like.delete()
            return Response({"message":"Like removed"},status=status.HTTP_200_OK)
        except:
                return Response({"message":"Try again"}, status= status.HTTP_404_NOT_FOUND)
        
        
class Search_Work_Posts(ListAPIView):
    serializer_class = Work_Serializer 
     
    def  get_queryset(self):
        key = self.kwargs.get('value')
        if key != "":
                queryset =  Work.objects.filter(
                        Q(user__first_name__icontains=key) | 
                        Q(location__icontains=key) | 
                        Q(description__icontains=key) 
                        
                        )
                
                return queryset
  
        
                
                    
             
             
             
             
                             
                        
