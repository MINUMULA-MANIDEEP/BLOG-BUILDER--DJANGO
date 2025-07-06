from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Blog(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    blog_name=models.CharField(max_length=100)
    blog_info=models.TextField()
    blog_date=models.DateTimeField(null=True,blank=True)
    blog_image=models.ImageField(upload_to="blog_images")
