import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .web_inference import process_image, process_video
from .models import DetectionHistory # Import your database
from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from .web_inference import process_image, process_video, generate_frames

def upload_and_detect(request):
    if request.method == 'POST' and request.FILES.get('media_file'):
        upload = request.FILES['media_file']
        
        fss = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        filename = fss.save(upload.name, upload)
        file_path = fss.path(filename)
        
        file_extension = os.path.splitext(filename)[1].lower()
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
        
        if file_extension in video_extensions:
            # Catch BOTH returns
            result_url, summary = process_video(file_path)
            media_type = 'video'
        else:
            # Catch BOTH returns
            result_url, summary = process_image(file_path)
            media_type = 'image'
            
        # Save the new summary to the database
        DetectionHistory.objects.create(
            media_type=media_type,
            original_filename=upload.name,
            result_url=result_url,
            detection_summary=summary # <--- Added this!
        )
            
        return render(request, 'detector/result.html', {
            'result_url': result_url,
            'media_type': media_type,
            'summary': summary # <--- Pass it to the HTML!
        })
        
    return render(request, 'detector/upload.html')

# --- The History View ---
def history_view(request):
    # Grab all records from the database, ordered by newest first
    records = DetectionHistory.objects.all().order_by('-created_at')
    return render(request, 'detector/history.html', {'records': records})

def clear_history(request):
    if request.method == 'POST':
        # 1. Wipe the database records
        DetectionHistory.objects.all().delete()
        
        # 2. Delete the physical files to save hard drive space
        uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        results_dir = os.path.join(settings.MEDIA_ROOT, 'results')
        
        for directory in [uploads_dir, results_dir]:
            if os.path.exists(directory):
                for filename in os.listdir(directory):
                    file_path = os.path.join(directory, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    except Exception:
                        pass # Silently skip any files currently locked by Windows
                        
    # Send the user back to the refreshed history page
    return redirect('history')

def live_webcam(request):
    """Renders the HTML page that will hold the video stream."""
    return render(request, 'detector/live_cam.html')

def video_feed(request):
    """The endless stream of JPEG frames sent to the browser."""
    return StreamingHttpResponse(
        generate_frames(), 
        content_type='multipart/x-mixed-replace; boundary=frame'
    )