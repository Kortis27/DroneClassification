from django.contrib import admin
from .models import DetectionHistory

# This makes your history visible in the Django admin panel
admin.site.register(DetectionHistory)