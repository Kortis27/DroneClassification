import os
import cv2
from ultralytics import YOLO
from django.conf import settings

# 1. Point to the shared model in the root directory
PROJECT_ROOT = os.path.dirname(settings.BASE_DIR) 
MODEL_PATH = os.path.join(PROJECT_ROOT, 'runs/detect/train2/weights/16_elm_84_rendered.pt')

# 2. Load the model globally so it doesn't have to be reloaded on every request
model = YOLO(MODEL_PATH)

def process_image(image_file_path):
    # 1. Run the AI Classification prediction
    results = model(image_file_path)
    
    # 2. Extract Classification Data
    if results[0].probs is not None:
        # Get the ID of the highest probability class
        top_class_id = results[0].probs.top1
        # Match it to the class name (e.g., "burden" or "no_burden")
        class_name = model.names[top_class_id]
        # Get the confidence percentage
        confidence = float(results[0].probs.top1conf)
        
        summary = f"{class_name.capitalize()} ({confidence:.0%})"
    else:
        summary = "Classification failed."

    # 3. Generate the new filename and paths
    original_filename = os.path.basename(image_file_path)
    new_filename = f"classified_{original_filename}"
    
    results_dir = os.path.join(settings.MEDIA_ROOT, 'results')
    os.makedirs(results_dir, exist_ok=True)
    save_path = os.path.join(results_dir, new_filename)
    
    # 4. Draw the classification text and save the new image
    annotated_image = results[0].plot()
    cv2.imwrite(save_path, annotated_image)
    
    # 5. Return both the URL for the webpage and the text for the database
    return f"/media/results/{new_filename}", summary


def process_video(video_file_path):
    cap = cv2.VideoCapture(video_file_path)
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    original_filename = os.path.basename(video_file_path)
    base_name = os.path.splitext(original_filename)[0]
    new_filename = f"classified_{base_name}.mp4"
    
    results_dir = os.path.join(settings.MEDIA_ROOT, 'results')
    os.makedirs(results_dir, exist_ok=True)
    save_path = os.path.join(results_dir, new_filename)
    
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))
    
    # --- NEW: Track the absolute highest confidence seen in the video ---
    highest_confidence = 0.0
    best_class_name = None
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        results = model.predict(frame, verbose=False)
        
        # Extract Classification Data for this frame
        if results[0].probs is not None:
            # Get the confidence of the top prediction for this frame
            current_confidence = float(results[0].probs.top1conf)
            
            # If this is the highest confidence we've seen so far, save it
            if current_confidence > highest_confidence:
                highest_confidence = current_confidence
                top_class_id = results[0].probs.top1
                best_class_name = model.names[top_class_id]
        
        # Write the annotated frame to the new video file
        annotated = results[0].plot()
        out.write(annotated)
        
    cap.release()
    out.release()
    
    if best_class_name:
        summary = f"{best_class_name.capitalize()} ({highest_confidence:.0%})"
    else:
        summary = "No objects classified."
    
    return f"/media/results/{new_filename}", summary
def generate_frames():
    """
    Captures live video, runs YOLO Classification, and yields JPEG frames.
    """

    camera = cv2.VideoCapture("http://192.168.4.72:4747/video") 
    
    while True:
        success, frame = camera.read()
        if not success:
            break
            
        # Run YOLO classification prediction
        # No conf=0.2 needed for classification
        results = model.predict(frame, verbose=False)
        
        # YOLO's plot() will automatically write the top classification 
        # (burden or no_burden) in the top corner of the video frame
        annotated_frame = results[0].plot()
        
        # Compress the image to JPEG for the web stream
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()
        
        # Yield the frame in the exact HTTP format required for MJPEG streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
               
    camera.release()