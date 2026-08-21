import cv2
from ultralytics import YOLO

model = YOLO("runs/detect/train-5/weights/best.pt")

# 讀取原始影片
cap = cv2.VideoCapture("videos/test video3.mp4")

# 取得原始影片資訊
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# 建立輸出影片
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

out = cv2.VideoWriter(
    "test video3 conf=0.20.mp4",
    fourcc,
    fps,
    (width, height)
)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame, conf=0.20)

    for result in results:
        for box in result.boxes:

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            conf = float(box.conf[0])

            # 畫框
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # 顯示文字
            text = f"vehicle {conf:.2f}"

            cv2.putText(
                frame,
                text,
                (x1, max(y1 - 5, 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0, 255, 0),
                2
            )

    # ★ 把這一幀寫進輸出影片
    out.write(frame)

    # 同時顯示
    cv2.imshow("Vehicle Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()

# ★ 儲存完成
out.release()

cv2.destroyAllWindows()
