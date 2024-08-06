from django.db import models

# Create your models here.

class BaseModel(models.Model):

    """ Base model to add extra fields created_at and updated_at to the child model"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Video(BaseModel):

    """ this model contains the information about uploaded video file and store this to videos folder in media folder"""
    
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='files/')
    pdf_file = models.FileField(upload_to='files/pdf/', null=True, blank=True)
    status = models.CharField(max_length=50, default="pending")
    uploaded_at = models.DateTimeField(auto_now_add=True)
