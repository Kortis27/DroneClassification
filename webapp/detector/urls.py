from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_and_detect, name='upload_and_detect'),
    path('history/', views.history_view, name='history'),
    path('clear-history/', views.clear_history, name='clear_history'),
    
    # NEW: The Webcam paths
    path('live-cam/', views.live_webcam, name='live_cam'),
    path('video-feed/', views.video_feed, name='video_feed'),
]