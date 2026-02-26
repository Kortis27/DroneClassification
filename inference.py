from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")

results = model("test2.jpg", conf=0.5)

results[0].show()   # display