from ultralytics import YOLO

print("Object Detection Started")

def detect_objects(image_path):
    model = YOLO("yolov8n.pt")

    results = model(image_path)

    print("Detection Completed")

    result = results[0]

    for box in result.boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        print(
            f"Detected: {model.names[class_id]} "
            f"Confidence: {confidence:.2f}"
        )

    result.show()

if __name__ == "__main__":
    detect_objects("sample_road.jpg")