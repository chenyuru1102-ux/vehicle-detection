import os
import random
import shutil

image_folder = "extracted_frames"
label_folder = "new_labels"

train_image_folder = "dataset/images/train"
val_image_folder = "dataset/images/val"

train_label_folder = "dataset/labels/train"
val_label_folder = "dataset/labels/val"

# 建立資料夾
os.makedirs(train_image_folder, exist_ok=True)
os.makedirs(val_image_folder, exist_ok=True)
os.makedirs(train_label_folder, exist_ok=True)
os.makedirs(val_label_folder, exist_ok=True)

# 找所有圖片
images = [
    f for f in os.listdir(image_folder)
    if f.endswith(".jpg")
]

# 固定亂數，讓每次切分結果一樣
random.seed(42)
random.shuffle(images)

# 80% train
split_index = int(len(images) * 0.8)

train_images = images[:split_index]
val_images = images[split_index:]

# 複製 train
for image_name in train_images:

    name = os.path.splitext(image_name)[0]

    shutil.copy(
        os.path.join(image_folder, image_name),
        os.path.join(train_image_folder, image_name)
    )

    shutil.copy(
        os.path.join(label_folder, name + ".txt"),
        os.path.join(train_label_folder, name + ".txt")
    )

# 複製 val
for image_name in val_images:

    name = os.path.splitext(image_name)[0]

    shutil.copy(
        os.path.join(image_folder, image_name),
        os.path.join(val_image_folder, image_name)
    )

    shutil.copy(
        os.path.join(label_folder, name + ".txt"),
        os.path.join(val_label_folder, name + ".txt")
    )

print("完成！")
print("全部：", len(images))
print("Train：", len(train_images))
print("Val：", len(val_images))