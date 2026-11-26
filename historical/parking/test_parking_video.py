import cv2
from ultralytics import YOLO

# 載入模型
model = YOLO("runs/detect/train-4/weights/best.pt")

# 預測
results = model.predict(
    source="dataset/images/val/parking2_003.jpg",
    conf=0.45,
    imgsz=416,
    save=True,
    show=False,
    line_width=3
)

# 取得 YOLO 畫好框的圖片
result_img = results[0].plot(line_width=3)



# 縮小「顯示」尺寸
h, w = result_img.shape[:2]

max_width = 1000

if w > max_width:
    scale = max_width / w
    display_img = cv2.resize(
        result_img,
        (int(w * scale), int(h * scale))
    )
else:
    display_img = result_img


# 顯示
cv2.imshow("YOLO Result", display_img)

# 等你按任意鍵才關閉
cv2.waitKey(0)
cv2.destroyAllWindows()