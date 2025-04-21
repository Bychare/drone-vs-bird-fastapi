from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from model.yolo_predict import load_model, predict_image
from utils.image_utils import save_uploaded_file
import uvicorn
import nest_asyncio
from pyngrok import ngrok, conf
import uuid
import os
import getpass


# Создание экземпляра FastAPI
app = FastAPI()

# Загрузка модели
model = load_model()
class_map = model.model.names

# Создание папки для статических файлов (изображений)
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html><head><title>Drone vs Bird</title></head>
    <body>
    <h1>Upload Image</h1>
    <form action="/predict/" enctype="multipart/form-data" method="post">
        <input name="file" type="file" accept="image/*">
        <input type="submit" value="Predict">
    </form>
    </body></html>
    """

# Обработка загрузки и предсказания
@app.post("/predict/", response_class=HTMLResponse)
async def predict(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    input_path = save_uploaded_file(file, file_id)
    output_path = predict_image(model, input_path)

    return f"""
    <html><body><h2>Prediction</h2>
    <img src="/{output_path}" style="max-width: 80%;">
    <p><a href="/">← Back</a></p></body></html>
    """

# Запуск FastAPI + Ngrok
if __name__ == "__main__":
    # Способ 1: Ввод токена через input() (более надежно, чем getpass)
    ngrok_token = input("Enter your ngrok authtoken: ").strip()
    
    # Убедитесь, что токен не пустой и применяется правильно
    if not ngrok_token:
        raise ValueError("Ngrok authtoken cannot be empty!")
    
    # Установка токена (вариант 1)
    conf.get_default().auth_token = ngrok_token
    
    # Альтернатива (вариант 2) - явно передать токен в connect()
    # public_url = ngrok.connect(8000, auth_token=ngrok_token)
    
    nest_asyncio.apply()
    
    try:
        public_url = ngrok.connect(8000)
        print("Public URL:", public_url)
        uvicorn.run(app, port=8000)
    except Exception as e:
        print(f"Ngrok error: {e}")
        print("Check your authtoken at: https://dashboard.ngrok.com/get-started/your-authtoken")
