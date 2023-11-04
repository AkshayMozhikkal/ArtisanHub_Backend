from django.contrib import admin
from .models import Message



class MessageAdmin(admin.ModelAdmin):
    list_display = ('message', 'sender', 'receiver')
    
  
admin.site.register(Message,MessageAdmin)