from django.shortcuts import render
from rest_framework.generics import *
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import date, timedelta
from django.db.models import Count


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
        
        
# class MonthlyPostCountView(ListAPIView):
#     serializer_class = WorkDateSerializer

#     def get_queryset(self):
        
#         year = self.kwargs.get('year')
#         month = self.kwargs.get('month')

        
#         start_date = date(int(year), int(month), 1)
#         if int(month) == 12:
#             end_date = date(int(year) + 1, 1, 1)
#         else:
#             end_date = date(int(year), int(month) + 1, 1)

        
#         queryset = Work.objects.filter(date__gte=start_date, date__lt=end_date).order_by('date')
#         return queryset        
  
        
# views.py
from rest_framework.response import Response

class MonthlyPostCountView(GenericAPIView):
    serializer_class = WorkDateSerializer

    def get(self, request, year, month):
        start_date = date(int(year), int(month), 1)
        if int(month) == 12:
            end_date = date(int(year) + 1, 1, 1)
        else:
            end_date = date(int(year), int(month) + 1, 1)

        queryset = Work.objects.filter(date__gte=start_date, date__lt=end_date)
        data = {}

        for work in queryset:
            date_str = work.date.strftime('%Y-%m-%d')
            if date_str in data:
                data[date_str] += 1
            else:
                data[date_str] = 1

        return Response(data)
                
                    
             
             
             
             
                             
                        
