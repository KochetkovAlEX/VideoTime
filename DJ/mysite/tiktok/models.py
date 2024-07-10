from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

   

    
class Video(models.Model):
    title = models.CharField(max_length=30)
    video = models.FileField(null=True, validators=[FileExtensionValidator(['mp4'])])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.JSONField(default=dict, blank=True)


class Post(models.Model):
    post = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, blank=True, null=True)
    