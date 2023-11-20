from django.shortcuts import render
from rest_framework.views import *
from rest_framework.generics import *
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from django.db.models import Q
from django.core.mail import send_mail
from decouple import config



# Create your views here.

# All connections
class Connections(ListAPIView):
    queryset = Connection.objects.all()
    serializer_class = Connections_Serializer


# Connections of a Single User
class UserConnectionsView(ListAPIView):
    serializer_class = Connected_Users_Serializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')  
        
        try:
            user = Uuser.objects.get(id=user_id)
        except Uuser.DoesNotExist:
            raise Http404

        queryset = Connection.objects.filter(
            from_user=user
        ).union(
            Connection.objects.filter(to_user=user)
        )

        return queryset
    
# Search in connections 
class Search_Connection(ListAPIView):
    serializer_class = Connected_Users_Serializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        search_key = self.kwargs.get('search_key')

        try:
            user = Uuser.objects.get(id=user_id)
        except Uuser.DoesNotExist:
            raise Http404

        queryset = Connection.objects.filter(
            Q(from_user=user) | Q(to_user=user),
            status='a'  
        )

        if search_key:
            queryset = queryset.filter(
                Q(from_user__first_name__icontains=search_key) |
                Q(from_user__last_name__icontains=search_key) |
                Q(from_user__username__icontains=search_key) |
                Q(to_user__first_name__icontains=search_key) |
                Q(to_user__last_name__icontains=search_key) |
                Q(to_user__username__icontains=search_key)
            )

        return queryset

    
# Connections of Current User
# class LoginedUserConnections(ListAPIView):
#     serializer_class = Connected_Users_Serializer

#     def get_queryset(self):
#         user = self.request.user  

#         queryset = Connection.objects.filter(
#             models.Q(from_user=user) | models.Q(to_user=user) 
#         )

#         return queryset 
    
   
class Connection_Status(RetrieveAPIView):
    queryset = Connection.objects.all()
    serializer_class = Connections_Serializer

    def retrieve(self, request, to_user_id, *args, **kwargs):
        from_user = request.user
        to_user_id = int(to_user_id)

        
        try:
            connection = Connection.objects.get(from_user=from_user, to_user_id=to_user_id)
            serializer = self.get_serializer(connection)
            return Response(serializer.data)
        except Connection.DoesNotExist:
            pass 
        
        try:
            connection = Connection.objects.get(from_user_id=to_user_id, to_user=from_user)
            serializer = self.get_serializer(connection)
            return Response(serializer.data)
        except Connection.DoesNotExist:
            return Response({"error": "Connection not found."}, status=status.HTTP_404_NOT_FOUND)


    
class Connection_Request(CreateAPIView):
    queryset = Connection.objects.all()
    serializer_class = Connections_Serializer

    
    def create(self, request, *args, **kwargs):
        from_user_id = request.data.get('from_user', None) 
        to_user_id = request.data.get('to_user', None)

        if from_user_id == to_user_id:
            return Response({"error": "You cannot send a request to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        existing_request = Connection.objects.filter(from_user_id=from_user_id, to_user_id=to_user_id, status='p').first()
        accepted_request = Connection.objects.filter(from_user_id=from_user_id, to_user_id=to_user_id, status='a').first()
        if existing_request:
            return Response({"error": "You've already sent a request to this user."}, status=status.HTTP_400_BAD_REQUEST)
        if accepted_request:
            return Response({"error": "You already have a connection with this user."}, status=status.HTTP_400_BAD_REQUEST)
        
        to_user_email = Uuser.objects.get(id=to_user_id).email
        name = Uuser.objects.get(id=from_user_id).first_name 
        subject = "ArtisanHub|Connection Request"
        message = f"You have received a connection request from {name}. Log in to your account to respond: {config('front_end_url')}login"
        from_email = 'akshay.for.career@gmail.com'
        
        send_mail(subject, message, from_email, [to_user_email])
        
        return super().create(request, *args, **kwargs)
    


class AcceptRejectConnection(RetrieveUpdateAPIView):
    queryset = Connection.objects.all()
    serializer_class = Connections_Serializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        status = request.data.get('status', None)
        

        if status not in ('a', 'r'):
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        if status == 'a':
            if instance.status != 'p':
                return Response({"error": "Cannot accept a request that is not pending."}, status=status.HTTP_400_BAD_REQUEST)
            instance.status = 'a'
            instance.save()
            return Response({"message": "Connection request accepted."})

        if status == 'r':
            if instance.status != 'p':
                return Response({"error": "Cannot reject a request that is not pending."}, status=status.HTTP_400_BAD_REQUEST)
            instance.status = 'r'
            instance.save()
            return Response({"message": "Connection request rejected."})
        
class Delete_Connection(DestroyAPIView):
    lookup_field = 'id'
    queryset= Connection.objects.all()
    serializer_class = Connections_Serializer
    
           
     
    
    
   