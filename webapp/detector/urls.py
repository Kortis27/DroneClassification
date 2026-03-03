from django.urls import path
from . import views

urlpatterns = [
    # This maps the root URL of the app to your view
    path('', views.upload_and_detect, name='upload_and_detect'),
]