from ultralytics import YOLO
import os

# 1. 載入官方 YOLO
model = YOLO("yolo11n.pt")

# 2. 圖片與標籤資料夾
image_folder = "extracted_frames"
label_folder = "labels"

os.makedirs(label_folder, exist_ok=True)

# 3. 一張一張圖片處理
for image_name in os.listdir(image_folder):

    if not image_name.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    image_path = os.path.join(image_folder, image_name)

    print("正在自動標註：", image_name)

    # 4. YOLO 預測
    results = model.predict(
        source=image_path,
        conf=0.05,
        imgsz=1280,
        verbose=False
    )

    result = results[0]

    # 5. 建立對應的 txt
    label_name = os.path.splitext(image_name)[0] + ".txt"
    label_path = os.path.join(label_folder, label_name)

    with open(label_path, "w") as f:

        for box in result.boxes:

            # COCO 裡 car=2, motorcycle=3, bus=5, truck=7
            class_id = int(box.cls[0])

            if class_id not in [2, 5, 7]:
                continue

            # YOLO 已經幫我們轉成 0~1 的 normalized xywh
            x_center, y_center, width, height = box.xywhn[0]

            # 我們自己的 dataset 全部統一成 class 0 = vehicle
            f.write(
                f"0 "
                f"{x_center.item():.6f} "
                f"{y_center.item():.6f} "
                f"{width.item():.6f} "
                f"{height.item():.6f}\n"
            )

print("自動標註完成！")