import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .web_inference import process_image  # Importing the YOLO script

def upload_and_detect(request):
    # Check if the user submitted the form with an image
    if request.method == 'POST' and request.FILES.get('image'):
        upload = request.FILES['image']
        
        # Save the uploaded file to the media/uploads/ folder
        fss = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        filename = fss.save(upload.name, upload)
        file_path = fss.path(filename)
        
        # Run the YOLO inference on the saved image
        result_url = process_image(file_path)
        
        # Render the result page, passing the URL of the new image
        return render(request, 'detector/result.html', {'result_image': result_url})
        
    # If they just visited the page, show them the upload form
    return render(request, 'detector/upload.html')