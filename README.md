# Vehicle Detection

A vehicle detection project using Python, OpenCV, and YOLO.

## Features

- Extract frames from videos
- Label vehicle images
- Train a custom YOLO model
- Perform vehicle detection on videos
- Visualize detection results

## Technologies

- Python
- OpenCV
- YOLO
- PyTorch

## Project Structure

- `extract_frames.py` - Extract frames from videos
- `label_images.py` - Create image annotations
- `check_label.py` - Check annotation results
- `split_dataset.py` - Split the dataset for training
- `train_yolo.py` - Train the YOLO model
- `predict_video.py` - Run vehicle detection on videos
- `predict_video_custom.py` - Run detection using a custom-trained model

## Installation

Install the required Python packages:

```bash
pip install ultralytics opencv-python torch
```

## Usage

Run vehicle detection on a video:

```bash
python predict_video.py
```

Run detection using a custom-trained YOLO model:

```bash
python predict_video_custom.py
```

## Model File
This project uses YOLO model weights (`.pt` files).

Model files are not included in this repository because they can be large.
Place the required model file in the project directory before running the detection scripts.