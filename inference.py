import cv2
from ultralytics import YOLO

model = YOLO("runs/detect/train2/weights/best.pt")

cap = cv2.VideoCapture(0)  # 0 = webcam

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(frame, conf=0.2, verbose=False)
    annotated = results[0].plot()  # Draw boxes on frame

    cv2.imshow("Drone Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):  # Press Q to quit
        break

cap.release()
cv2.destroyAllWindows()