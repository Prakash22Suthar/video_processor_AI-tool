from django.contrib import admin
from .models import Video
# Register your models here.

@admin.register(Video)
class UserVideo(admin.ModelAdmin):
    list_display = ["id", "title", "video_file", "uploaded_at"]
    list_display_links = ["title"]
