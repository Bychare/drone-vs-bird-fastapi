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

# Initialize FastAPI app and load model\ app = FastAPI()
model = load_model()
class_map = model.model.names

# Ensure static directory exists and mount it for serving images
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Home page route with upload form
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

# Prediction endpoint: saves the file, runs model, shows result
@app.post("/predict/", response_class=HTMLResponse)
async def predict(file: UploadFile = File(...)):
    # Generate a unique filename
    file_id = str(uuid.uuid4())

    # Save the uploaded file to static folder
    input_path = save_uploaded_file(file, file_id)

    # Run prediction and get output path
    output_path = predict_image(model, input_path)

    # Return HTML page with result image
    return f"""
    <html><body><h2>Prediction</h2>
    <img src="/{output_path}" style="max-width: 80%;">
    <p><a href="/">← Back</a></p>
    </body></html>
    """

# Main entrypoint: setup ngrok and run server
if __name__ == "__main__":
    # Securely prompt user for ngrok auth token (not stored in code)
    token = getpass.getpass("Enter your ngrok authtoken: ")
    conf.get_default().auth_token = token

    # Allow nested asyncio event loop for ngrok
    nest_asyncio.apply()

    # Open public tunnel to local port
    public_url = ngrok.connect(8000)
    print("Public URL:", public_url)

    # Run Uvicorn ASGI server
    uvicorn.run(app, port=8000)
