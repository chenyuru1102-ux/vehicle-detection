from ultralytics import YOLO

model = YOLO("yolo11n.pt")

results = model.predict(
    source="tile1.jpg",
    save=True,
    conf=0.05,
    imgsz=1280,
    line_width =3,
    show_labels = False,
    show_conf = False
)

print("Detection finished!")