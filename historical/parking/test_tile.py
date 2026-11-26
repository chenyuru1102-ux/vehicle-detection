import cv2

cap = cv2.VideoCapture("videos/parking3.mp4")

ret, frame = cap.read()

if not ret:
    print("讀取影片失敗")
    exit()

height, width = frame.shape[:2]

print("width =", width)
print("height =", height)

half_w = width // 2
half_h = height // 2

tile1 = frame[0:half_h, 0:half_w]
tile2 = frame[0:half_h, half_w:width]
tile3 = frame[half_h:height, 0:half_w]
tile4 = frame[half_h:height, half_w:width]

cv2.imwrite("tile1.jpg", tile1)
cv2.imwrite("tile2.jpg", tile2)
cv2.imwrite("tile3.jpg", tile3)
cv2.imwrite("tile4.jpg", tile4)

cap.release()

print("切割完成")
