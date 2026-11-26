import cv2
import os

cap = cv2.VideoCapture("videos/Cars drive on street.mp4")

os.makedirs("images", exist_ok=True)
os.makedirs("labels", exist_ok=True)

frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("Video", frame)

    key = cv2.waitKey(30) & 0xFF

    if key == ord("s"):

        height, width = frame.shape[:2]

        labels = []

        while True:
            x, y, w, h = cv2.selectROI(
                "Select Object",
                frame,
                False
            )

            # 如果沒有框東西，就結束
            if w == 0 or h == 0:
                break

            x_center = (x + w / 2) / width
            y_center = (y + h / 2) / height
            yolo_w = w / width
            yolo_h = h / height

            label = f"0 {x_center} {y_center} {yolo_w} {yolo_h}"

            labels.append(label)

            print("加入標註：", label)

        image_name = f"frame_{frame_count:04d}.jpg"
        label_name = f"frame_{frame_count:04d}.txt"

        cv2.imwrite(
            os.path.join("images", image_name),
            frame
        )

        with open(
            os.path.join("labels", label_name),
            "w"
        ) as f:

            for label in labels:
                f.write(label + "\n")

        print("已儲存：", image_name)
        print("物件數量：", len(labels))

        frame_count += 1

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()