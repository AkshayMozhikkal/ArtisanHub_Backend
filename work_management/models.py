from django.db import models
from user_management.models import Uuser

# Create your models here.
class Work(models.Model):
    user = models.ForeignKey(Uuser, on_delete=models.CASCADE )  
    title = models.CharField( max_length=100) 
    image = models.ImageField(upload_to="work_posts" , blank=True, null=True)
    description = models.TextField(blank=True, null=True) 
    location = models.CharField(max_length=150)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100, default="pending")
    
    def get_comment_count(self):
        return Comment.objects.filter(post=self).count()

    def get_like_count(self):
        return Like.objects.filter(post=self).count()
    
    
    
class Comment(models.Model):
    post = models.ForeignKey(Work, on_delete=models.CASCADE) 
    commented_by = models.ForeignKey(Uuser, on_delete=models.CASCADE)
    text = models.TextField()   
    commented_at = models.DateTimeField(auto_now_add=True)
    
class Like(models.Model):
    post = models.ForeignKey(Work, on_delete=models.CASCADE) 
    liked_by = models.ForeignKey(Uuser, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['post', 'liked_by'] 
        