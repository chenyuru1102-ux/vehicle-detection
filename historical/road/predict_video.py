from ultralytics import YOLO

model = YOLO("runs/detect/train-5/weights/best.pt")

model.predict(
    source="videos/night car.mp4",
    conf=0.25,
    show=True,
    save=True
)