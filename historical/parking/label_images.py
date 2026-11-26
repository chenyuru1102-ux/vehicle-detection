import cv2
import os
from ultralytics import YOLO

# =========================
# 基本設定
# =========================

image_folder = "extracted_frames"
label_folder = "labels"

os.makedirs(label_folder, exist_ok=True)

# 自己的資料集只有一類：vehicle
CLASS_ID = 0

# YOLO 預標註 confidence
YOLO_CONF = 0.01

# COCO 類別
# 2 = car
# 5 = bus
# 7 = truck
YOLO_CLASSES = [2, 5, 7]

# 載入 YOLO 官方模型
model = YOLO("yolo11n.pt")


# =========================
# 讀取圖片清單
# =========================

image_files = sorted([
    f for f in os.listdir(image_folder)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
])

if not image_files:
    print("找不到圖片")
    exit()

current_index = 0
boxes = []

drawing = False
start_x, start_y = 0, 0
current_x, current_y = 0, 0


# =========================
# 計算兩個框的 IoU
# 用來避免 YOLO 重複加入同一台車
# =========================

def calculate_iou(box1, box2):

    x1_1, y1_1, x2_1, y2_1 = box1
    x1_2, y1_2, x2_2, y2_2 = box2

    inter_x1 = max(x1_1, x1_2)
    inter_y1 = max(y1_1, y1_2)

    inter_x2 = min(x2_1, x2_2)
    inter_y2 = min(y2_1, y2_2)

    inter_width = max(0, inter_x2 - inter_x1)
    inter_height = max(0, inter_y2 - inter_y1)

    intersection = inter_width * inter_height

    area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
    area2 = (x2_2 - x1_2) * (y2_2 - y1_2)

    union = area1 + area2 - intersection

    if union == 0:
        return 0

    return intersection / union


# =========================
# 載入既有 label
# =========================

def load_labels(image_name, img_width, img_height):

    global boxes

    boxes = []

    label_name = os.path.splitext(image_name)[0] + ".txt"
    label_path = os.path.join(label_folder, label_name)

    if not os.path.exists(label_path):
        return False

    with open(label_path, "r") as f:

        for line in f:

            parts = line.strip().split()

            if len(parts) != 5:
                continue

            class_id, x_center, y_center, width, height = map(
                float,
                parts
            )

            x_center *= img_width
            y_center *= img_height

            width *= img_width
            height *= img_height

            x1 = int(x_center - width / 2)
            y1 = int(y_center - height / 2)

            x2 = int(x_center + width / 2)
            y2 = int(y_center + height / 2)

            boxes.append(
                (x1, y1, x2, y2)
            )

    print(
        f"讀取原本標註：{image_name}，"
        f"{len(boxes)} 個框"
    )

    return True


# =========================
# YOLO 自動預標註
# =========================

def auto_label_with_yolo(image):

    global boxes

    print("YOLO 正在幫忙找車...")

    results = model.predict(
        source=image,
        conf=YOLO_CONF,
        classes=YOLO_CLASSES,
        verbose=False
    )

    added_count = 0

    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            xyxy = box.xyxy[0].cpu().numpy()

            x1 = int(xyxy[0])
            y1 = int(xyxy[1])
            x2 = int(xyxy[2])
            y2 = int(xyxy[3])

            new_box = (
                x1,
                y1,
                x2,
                y2
            )

            # =========================
            # 檢查是否跟原本框重複
            # =========================

            duplicate = False

            for old_box in boxes:

                iou = calculate_iou(
                    new_box,
                    old_box
                )

                # IoU > 0.5 視為同一台車
                if iou > 0.5:
                    duplicate = True
                    break

            # 沒重複才新增
            if not duplicate:

                boxes.append(new_box)

                added_count += 1

    print(
        f"YOLO 新增 {added_count} 個框，"
        f"目前總共 {len(boxes)} 個框"
    )


# =========================
# 儲存 YOLO label
# =========================

def save_labels(
    image_name,
    img_width,
    img_height
):

    label_name = (
        os.path.splitext(image_name)[0]
        + ".txt"
    )

    label_path = os.path.join(
        label_folder,
        label_name
    )

    with open(label_path, "w") as f:

        for x1, y1, x2, y2 in boxes:

            box_width = x2 - x1
            box_height = y2 - y1

            x_center = x1 + box_width / 2
            y_center = y1 + box_height / 2

            # YOLO 格式正規化 0~1
            x_center /= img_width
            y_center /= img_height

            box_width /= img_width
            box_height /= img_height

            f.write(
                f"{CLASS_ID} "
                f"{x_center:.6f} "
                f"{y_center:.6f} "
                f"{box_width:.6f} "
                f"{box_height:.6f}\n"
            )

    print(
        "已儲存：",
        label_path
    )


# =========================
# 滑鼠事件
# =========================

def mouse_callback(
    event,
    x,
    y,
    flags,
    param
):

    global drawing
    global start_x, start_y
    global current_x, current_y
    global boxes

    # =========================
    # 右鍵：刪除點到的框
    # =========================

    if event == cv2.EVENT_RBUTTONDOWN:

        for i in range(
            len(boxes) - 1,
            -1,
            -1
        ):

            x1, y1, x2, y2 = boxes[i]

            if (
                x1 <= x <= x2
                and
                y1 <= y <= y2
            ):

                removed = boxes.pop(i)

                print(
                    "刪除框：",
                    removed
                )

                return

    # =========================
    # 左鍵：新增框
    # =========================

    elif event == cv2.EVENT_LBUTTONDOWN:

        drawing = True

        start_x = x
        start_y = y

        current_x = x
        current_y = y

    elif event == cv2.EVENT_MOUSEMOVE:

        if drawing:

            current_x = x
            current_y = y

    elif event == cv2.EVENT_LBUTTONUP:

        drawing = False

        end_x = x
        end_y = y

        x1 = min(start_x, end_x)
        y1 = min(start_y, end_y)

        x2 = max(start_x, end_x)
        y2 = max(start_y, end_y)

        if (
            x2 - x1 > 5
            and
            y2 - y1 > 5
        ):

            boxes.append(
                (x1, y1, x2, y2)
            )

            print(
                "新增框：",
                boxes[-1]
            )


# =========================
# 主程式
# =========================

cv2.namedWindow(
    "YOLO Label Tool",
    cv2.WINDOW_NORMAL
)

cv2.setMouseCallback(
    "YOLO Label Tool",
    mouse_callback
)


while True:

    image_name = image_files[
        current_index
    ]

    image_path = os.path.join(
        image_folder,
        image_name
    )

    image = cv2.imread(
        image_path
    )

    if image is None:

        print(
            "讀取失敗：",
            image_name
        )

        break

    img_height, img_width = (
        image.shape[:2]
    )

    # =========================
    # 先讀取以前的標註
    # =========================

    has_existing_label = load_labels(
        image_name,
        img_width,
        img_height
    )

    # =========================
    # 沒有以前標註才自動叫 YOLO 框
    # 這樣不會破壞以前的資料
    # =========================

    if not has_existing_label:

        auto_label_with_yolo(
            image
        )

    while True:

        display = image.copy()

        # =========================
        # 已完成的框
        # =========================

        for x1, y1, x2, y2 in boxes:

            cv2.rectangle(
                display,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

        # =========================
        # 正在拖曳中的框
        # =========================

        if drawing:

            cv2.rectangle(
                display,
                (start_x, start_y),
                (current_x, current_y),
                (0, 255, 255),
                2
            )

        info = (
            f"{current_index + 1}"
            f"/{len(image_files)}  "
            f"{image_name}  "
            f"Boxes: {len(boxes)}"
        )

        cv2.putText(
            display,
            info,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        help_text = (
            "A: YOLO  "
            "S: Save  "
            "N: Next  "
            "P: Prev  "
            "Z: Undo  "
            "Q: Quit"
        )

        cv2.putText(
            display,
            help_text,
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

        cv2.imshow(
            "YOLO Label Tool",
            display
        )

        key = cv2.waitKey(20) & 0xFF

        # =========================
        # A = YOLO 再幫忙找車
        # 不會清掉原本的框
        # =========================

        if key == ord("a"):

            auto_label_with_yolo(
                image
            )

        # =========================
        # S = 儲存
        # =========================

        elif key == ord("s"):

            save_labels(
                image_name,
                img_width,
                img_height
            )

        # =========================
        # Z = 刪除上一個框
        # =========================

        elif key == ord("z"):

            if boxes:

                removed = boxes.pop()

                print(
                    "刪除：",
                    removed
                )

        # =========================
        # N = 儲存 + 下一張
        # =========================

        elif key == ord("n"):

            save_labels(
                image_name,
                img_width,
                img_height
            )

            if (
                current_index
                <
                len(image_files) - 1
            ):

                current_index += 1

            break

        # =========================
        # P = 儲存 + 上一張
        # =========================

        elif key == ord("p"):

            save_labels(
                image_name,
                img_width,
                img_height
            )

            if current_index > 0:

                current_index -= 1

            break

        # =========================
        # Q = 儲存 + 離開
        # =========================

        elif key == ord("q"):

            save_labels(
                image_name,
                img_width,
                img_height
            )

            cv2.destroyAllWindows()

            exit()