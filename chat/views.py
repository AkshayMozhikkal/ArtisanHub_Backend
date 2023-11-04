from django.shortcuts import render
from rest_framework.generics import *
from rest_framework.filters import SearchFilter
from .serializers import *
from user_management.models import *
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status



class PreviousMessagesView(ListAPIView):
    serializer_class = MessageSerializer
    pagination_class = None

    def get_queryset(self):
        user1 = int(self.kwargs['user1'])
        user2 = int(self.kwargs['user2'])

        thread_suffix = f"{user1}_{user2}" if user1 > user2 else f"{user2}_{user1}"
        thread_name = 'chat_'+thread_suffix
        queryset = Message.objects.filter(
            thread_name=thread_name
        )
        return queryset
    
class SingleUserChatsView(ListAPIView):
    serializer_class = ChatSerializer 
    
    def get(self, request, *args, **kwargs):
        userID = self.kwargs['id']
        user = Uuser.objects.get(id=userID)
        chat_count = Message.objects.filter(sender=user).union(Message.objects.filter(receiver=user)).count()
        return Response({"chat_count": chat_count}, status=status.HTTP_200_OK)