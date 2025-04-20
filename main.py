from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from model.yolo_predict import load_model, predict_image
from utils.image_utils import save_uploaded_file
import uvicorn
import nest_asyncio
from pyngrok import ngrok, conf
import uuid
import os

app = FastAPI()
model = load_model()
class_map = model.model.names

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html><head><title>Drone vs Bird</title></head>
    <body><h1>Upload Image</h1><form action="/predict/" enctype="multipart/form-data" method="post">
    <input name="file" type="file" accept="image/*"><input type="submit" value="Predict"></form></body></html>
    """

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

# Ngrok setup
conf.get_default().auth_token = "YOUR_NGROK_TOKEN"
nest_asyncio.apply()
public_url = ngrok.connect(8000)
print("Public URL:", public_url)
uvicorn.run(app, port=8000)
