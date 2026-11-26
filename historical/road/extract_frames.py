import cv2
import os

video_folder = "videos"
output_folder = "extracted_frames"

os.makedirs(output_folder, exist_ok=True)

# 每隔幾秒截一張
interval_seconds = 2

frame_count = 0

for video_name in os.listdir(video_folder):

    # 只處理影片檔
    if not video_name.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
        continue

    video_path = os.path.join(video_folder, video_name)

    print("正在處理：", video_name)

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)

    # 例如 30 FPS × 2 秒 = 每 60 frame 截一張
    interval_frames = int(fps * interval_seconds)

    current_frame = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        if current_frame % interval_frames == 0:

            file_name = f"frame_{frame_count:04d}.jpg"

            save_path = os.path.join(
                output_folder,
                file_name
            )

            cv2.imwrite(save_path, frame)

            print("儲存：", file_name)

            frame_count += 1

        current_frame += 1

    cap.release()

print("完成！")
print("總共截出", frame_count, "張圖片")