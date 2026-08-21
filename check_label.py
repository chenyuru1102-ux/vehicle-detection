import cv2
import os
import glob

image_folder = "extracted_frames"
label_folder = "new_labels"

image_paths = sorted(
    glob.glob(os.path.join(image_folder, "*.jpg"))
)

for image_path in image_paths:

    image_name = os.path.basename(image_path)
    name = os.path.splitext(image_name)[0]

    label_path = os.path.join(
        label_folder,
        name + ".txt"
    )

    img = cv2.imread(image_path)

    if img is None:
        print("圖片讀取失敗：", image_name)
        continue

    if not os.path.exists(label_path):
        print("找不到 label：", image_name)
        continue

    height, width = img.shape[:2]

    with open(label_path, "r") as f:
        lines = f.readlines()

    for line in lines:

        class_id, x_center, y_center, box_w, box_h = map(
            float,
            line.split()
        )

        x_center *= width
        y_center *= height
        box_w *= width
        box_h *= height

        x1 = int(x_center - box_w / 2)
        y1 = int(y_center - box_h / 2)

        x2 = int(x_center + box_w / 2)
        y2 = int(y_center + box_h / 2)

        cv2.rectangle(
            img,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

    print("正在檢查：", image_name)




    # ★ 永遠使用同一個視窗名稱
    cv2.imshow("Check Label", img)

    key = cv2.waitKey(0) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()