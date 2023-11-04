from django.urls import path
from .views import *
urlpatterns = [
    path("user-previous-chats/<int:user1>/<int:user2>/", PreviousMessagesView.as_view()),
    path("single_user_chats/<int:id>/", SingleUserChatsView.as_view(), name="single_user_chats"),

]