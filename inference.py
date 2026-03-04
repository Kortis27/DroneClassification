from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")

results = model("testimages/test5.jpg", conf=0.2)

results[0].show()   # display