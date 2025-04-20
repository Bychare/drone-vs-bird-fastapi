# Drone vs Bird Detection with YOLOv8 and FastAPI

This project uses a YOLOv8 model to classify and localize drones or birds in images. It includes a FastAPI web service and a public ngrok tunnel for live inference.

## Features

- Image detection using pretrained YOLOv8
- FastAPI web interface with image upload and prediction
- Ngrok tunnel for public access
- Animated GIF visualization of detections

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

Run the FastAPI server:
  uvicorn main.main:app --reload

Start ngrok tunnel:
  ngrok http 8000
