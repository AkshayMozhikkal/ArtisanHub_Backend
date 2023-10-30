from django.db import models
from user_management.models import *

# Create your models here.

class Connection(models.Model):
    from_user = models.ForeignKey(Uuser,related_name='friend_requests_sent', on_delete=models.CASCADE )
    to_user = models.ForeignKey(Uuser,related_name='friend_requests_received', on_delete=models.CASCADE )
    status = models.CharField(max_length=1, default='p', choices=(('p', 'Pending'), ('a', 'Accepted'), ('r', 'Rejected')))
    created_at = models.DateTimeField(auto_now_add=True)
    
    

