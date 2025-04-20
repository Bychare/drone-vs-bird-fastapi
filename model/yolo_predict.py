from ultralytics import YOLO

def load_model():
    return YOLO("yolov8x.pt")

def predict_image(model, image_path):
    results = model(image_path)
    output_path = image_path.replace(".jpg", "_result.jpg")
    results[0].save(filename=output_path)
    return output_path
