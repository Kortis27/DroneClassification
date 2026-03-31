from django.db import models

class DetectionHistory(models.Model):
    MEDIA_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES)
    original_filename = models.CharField(max_length=255)
    result_url = models.CharField(max_length=255)
    
    # --- NEW: Store the text summary ---
    # null=True, blank=True prevents errors with your older history records
    detection_summary = models.CharField(max_length=500, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_type.capitalize()} processed on {self.created_at.strftime('%Y-%m-%d %H:%M')}"