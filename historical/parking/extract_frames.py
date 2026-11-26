import cv2
import os
import numpy as np

video_folder = "videos"
output_folder = "extracted_frames"

os.makedirs(output_folder, exist_ok=True)

# 畫面差異門檻
difference_threshold = 15

for video_name in os.listdir(video_folder):

    if not video_name.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
        continue

    video_path = os.path.join(video_folder, video_name)

    print("正在處理：", video_name)

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)

    # 先每 1 秒檢查一次
    interval_frames = int(fps)

    current_frame = 0
    saved_count = 0

    previous_saved_gray = None

    video_stem = os.path.splitext(video_name)[0]

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if current_frame % interval_frames == 0:

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if previous_saved_gray is None:
                should_save = True

            else:
                diff = cv2.absdiff(gray, previous_saved_gray)

                mean_difference = np.mean(diff)

                print("畫面差異：", mean_difference)

                should_save = mean_difference > difference_threshold

            if should_save:

                output_name = f"{video_stem}_{saved_count:03d}.jpg"

                output_path = os.path.join(
                    output_folder,
                    output_name
                )

                cv2.imwrite(output_path, frame)

                previous_saved_gray = gray.copy()

                saved_count += 1

        current_frame += 1

    cap.release()

    print(f"{video_name} 完成，共儲存 {saved_count} 張")

print("全部完成")