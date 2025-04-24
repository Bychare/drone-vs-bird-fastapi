# Drone vs Bird Detection with YOLOv8 and FastAPI

This project uses a YOLOv8 model to classify and localize drones or birds in images. It includes a FastAPI web service and a public ngrok tunnel for live inference.

## Features

- Image detection using pretrained YOLOv8
- FastAPI web interface with image upload and prediction
- Ngrok tunnel for public access
- Animated GIF visualization of detections

```
drone-vs-bird-fastapi/
├── main.py                          # Основной файл FastAPI + ngrok
├── model/
│   └── yolo_predict.py             # Загрузка модели и предсказания
├── utils/
│   ├── image_utils.py              # Работа с изображениями и выборка
│   └── animation.py                # Создание gif-анимации
├── notebooks/
│   └── drone_vs_bird.ipynb         # Оригинальный ноутбук (перенос вручную)
├── requirements.txt
└── README.md
```

## Setup and Running Instructions  

1. **Clone the repository (if needed) or navigate to the project**  
   ```bash
   git clone https://github.com/Bychare/drone-vs-bird-fastapi.git  
   cd drone-vs-bird-fastapi  
   ```  

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt  
   ```  

3. **Run the server**  
   ```bash
   python main.py  
   ```  
   - If the Ngrok token is not saved yet, the script will prompt:  
     ```
     Enter your ngrok authtoken:
     ```  

4. **Access the public URL**  
   - Open in your browser:  
     - `http://127.0.0.1:8000/`  
     - or `http://localhost:8000`  
   - Upload an image on the main page  
   - Verify that:  
     - Predictions are displayed correctly  
     - Bounding boxes are drawn  
