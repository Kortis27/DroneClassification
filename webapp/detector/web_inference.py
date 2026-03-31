import os
import cv2
from ultralytics import YOLO
from django.conf import settings

# 1. Point to the shared model in the root directory
PROJECT_ROOT = os.path.dirname(settings.BASE_DIR) 
MODEL_PATH = os.path.join(PROJECT_ROOT, 'runs/detect/train2/weights/best.pt')

# 2. Load the model globally so it doesn't have to be reloaded on every request
model = YOLO(MODEL_PATH)

def process_image(image_file_path):
    # 1. Run the AI prediction
    results = model(image_file_path, conf=0.2)
    
    # 2. Extract Text Data for the database
    detected_items = []
    for box in results[0].boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        confidence = float(box.conf[0])
        detected_items.append(f"{class_name.capitalize()} ({confidence:.0%})")
    
    # Create the text summary
    if detected_items:
        summary = ", ".join(detected_items)
    else:
        summary = "No objects detected."

    # 3. Generate the new filename and paths
    original_filename = os.path.basename(image_file_path)
    new_filename = f"detected_{original_filename}"
    
    results_dir = os.path.join(settings.MEDIA_ROOT, 'results')
    os.makedirs(results_dir, exist_ok=True)
    save_path = os.path.join(results_dir, new_filename)
    
    # 4. Draw the boxes and save the new image
    annotated_image = results[0].plot()
    cv2.imwrite(save_path, annotated_image)
    
    # 5. Return both the URL for the webpage and the text for the database
    return f"/media/results/{new_filename}", summary

def process_video(video_file_path):
    """
    Takes an uploaded video, runs YOLO inference frame-by-frame,
    and saves the output as a web-friendly .webm video.
    """
    cap = cv2.VideoCapture(video_file_path)
    
    # Get original video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Force the output to be an .mp4 file
    original_filename = os.path.basename(video_file_path)
    base_name = os.path.splitext(original_filename)[0]
    new_filename = f"detected_{base_name}.mp4"
    
    results_dir = os.path.join(settings.MEDIA_ROOT, 'results')
    os.makedirs(results_dir, exist_ok=True)
    save_path = os.path.join(results_dir, new_filename)
    
    # Use mp4v codec for standard MP4 creation
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))
    
    unique_detections = set() # Use a set to avoid thousands of duplicates
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        results = model.predict(frame, conf=0.2, verbose=False)
        
        # --- NEW: Extract Video Text Data ---
        for box in results[0].boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            unique_detections.add(class_name.capitalize())
        # ------------------------------------
        
        annotated = results[0].plot()
        out.write(annotated)
        
    cap.release()
    out.release()
    
    # Create a summary of everything seen in the video
    if unique_detections:
        summary = "Detected in video: " + ", ".join(unique_detections)
    else:
        summary = "No objects detected."
    
    # Return BOTH the URL and the summary
    return f"/media/results/{new_filename}", summary

def generate_frames():
    """
    Captures live video, runs YOLO, and yields JPEG frames for web streaming.
    """
    # Change '0' to your phone's IP camera URL if you went that route!
    camera = cv2.VideoCapture(0)
    
    while True:
        success, frame = camera.read()
        if not success:
            break
            
        # Run YOLO inference (using 0.2 confidence to match your video script)
        results = model.predict(frame, conf=0.2, verbose=False)
        annotated_frame = results[0].plot()
        
        # Compress the image to JPEG
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()
        
        # Yield the frame in the exact HTTP format required for MJPEG streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
               
    camera.release()