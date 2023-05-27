from ultralytics import YOLO

# Load a model
model = YOLO('../support/yolov8n_best.pt')  # load an official model
model = YOLO('runs/detect/yolov8n_cars_custom/weights/best.pt')  # load a custom model

# Predict with the model
results = model('images/1.jpg')  # predict on an image