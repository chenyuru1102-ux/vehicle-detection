import cv2
import os
import glob

image_folder = "extracted_frames"
label_folder = "new_labels"

os.makedirs(label_folder, exist_ok=True)

# 找出所有 jpg，並按照檔名排序
image_paths = sorted(glob.glob(os.path.join(image_folder, "*.jpg")))

print("找到", len(image_paths), "張圖片")


for image_path in image_paths:

    # 取得檔名
    image_name = os.path.basename(image_path)

    # frame_0000.jpg → frame_0000
    name = os.path.splitext(image_name)[0]

    label_path = os.path.join(
        label_folder,
        name + ".txt"
    )

    # 如果已經標過，就跳過
    if os.path.exists(label_path):
        print("已標註，跳過：", image_name)
        continue

    img = cv2.imread(image_path)

    if img is None:
        print("讀取失敗：", image_name)
        continue

    height, width = img.shape[:2]

    labels = []

    print("\n目前圖片：", image_name)
    print("框車後按 ENTER / SPACE")
    print("不想再框車時按 C")

    while True:

        x, y, w, h = cv2.selectROI(
            "Label Vehicle",
            img,
            False
        )

        # 按 C 取消 selectROI 時
        # 通常會得到 0, 0, 0, 0
        if w == 0 or h == 0:
            break

        # -----------------------
        # Bounding Box → YOLO
        # -----------------------

        x_center = (x + w / 2) / width
        y_center = (y + h / 2) / height
        yolo_w = w / width
        yolo_h = h / height

        labels.append(
            f"0 {x_center} {y_center} {yolo_w} {yolo_h}"
        )

        # 把剛剛標好的框畫出來
        cv2.rectangle(
            img,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        print("已標：", len(labels), "台 vehicle")

    # -----------------------
    # 儲存 txt
    # -----------------------

    with open(label_path, "w") as f:

        for label in labels:
            f.write(label + "\n")

    print(
        "完成：",
        image_name,
        "共",
        len(labels),
        "台 vehicle"
    )

cv2.destroyAllWindows()

print("\n全部標註完成！")