from django.urls import path, include
# from . import views
from .views import UserLogin, UserSignupView, ProcessVideoView, DownloadPdfView, ProfileView

app_name = "video_app"

urlpatterns = [
    path('login/', UserLogin.as_view(), name="login"),
    path('signup/', UserSignupView.as_view(), name="signup"),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path('extract-audio/<int:pk>', ProcessVideoView.as_view(), name='process_video'),
    path('download-pdf/<int:pk>', DownloadPdfView.as_view(), name='download_pdf'),
    
    # path('', views.home_page, name='home'),
    # path('upload/', views.upload_video, name='upload_video'),
    # path('process/<int:pk>', views.process_video, name='process_video'),
]
