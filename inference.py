from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")

results = model("testimages/test6.jpg", conf=0.7)

results[0].show()   # display