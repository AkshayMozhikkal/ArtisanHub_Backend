from django.contrib import admin
from user_management.models import Uuser, Address



class UuserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active')
    
class AddressAdmin(admin.ModelAdmin):
    list_display = ('home', 'city')    


# Register your models here.

admin.site.register(Uuser, UuserAdmin)
admin.site.register(Address, AddressAdmin)

