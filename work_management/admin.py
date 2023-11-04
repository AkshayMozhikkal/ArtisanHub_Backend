from django.contrib import admin
from .models import Work



class WorkModel(admin.ModelAdmin):
    list_display = ('location', 'user', 'description')
    
  
admin.site.register(Work,WorkModel)