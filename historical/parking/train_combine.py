from ultralytics import YOLO

model = YOLO("yolo11n.pt")

model.train(
    data="dataset/data_combine.yaml",
    epochs=50,
    imgsz=416,
    batch=4,
    device="cpu"
)