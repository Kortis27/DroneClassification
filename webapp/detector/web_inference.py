import os
import cv2
from ultralytics import YOLO
from django.conf import settings

# 1. Point to the shared model in the root directory
PROJECT_ROOT = os.path.dirname(settings.BASE_DIR) 
MODEL_PATH = os.path.join(PROJECT_ROOT, 'yolov8n.pt')

# 2. Load the model globally so it doesn't have to be reloaded on every request
model = YOLO(MODEL_PATH)

def process_image(image_file_path):
    """
    Takes the path to an uploaded image, runs YOLO inference, 
    and saves the resulting image.
    """
    # Run the model - conf needs to be adjusted based on your needs and model performance
    results = model(image_file_path, conf=0.5)
    
    # Extract the image array with the bounding boxes drawn on it
    result_image_array = results[0].plot() 
    
    # Create the results directory if it doesn't exist yet
    results_dir = os.path.join(settings.MEDIA_ROOT, 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Create a path to save the new image
    filename = os.path.basename(image_file_path)
    save_path = os.path.join(results_dir, f"detected_{filename}")
    
    # Save it to the results folder using OpenCV
    cv2.imwrite(save_path, result_image_array)
    
    # Return the relative path so Django can display it in the browser
    return f"/media/results/detected_{filename}"