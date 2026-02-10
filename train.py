from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # nano = fastest
model.train(
    data="datasets/drone/drone.yaml",
    epochs=50,
    imgsz=640,
    batch=16
)