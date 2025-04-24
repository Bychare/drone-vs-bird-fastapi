from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
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
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
    <head>
        <title>Drone vs Bird</title>
        <style>
            .drop-zone {
                border: 3px dashed #ccc;
                padding: 2rem;
                text-align: center;
                margin: 1rem 0;
                transition: all 0.3s;
            }
            .drop-zone.dragover {
                border-color: #4CAF50;
                background: #f8f9fa;
            }
            #preview {
                max-width: 300px;
                margin: 1rem 0;
            }
            .hidden { display: none; }
        </style>
    </head>
    <body>
        <h1>Drone vs Bird Detector</h1>
        <form id="uploadForm" action="/predict/" enctype="multipart/form-data" method="post">
            <div class="drop-zone" id="dropZone">
                <p>Перетащите изображение сюда или кликните для выбора</p>
                <input type="file" name="file" id="fileInput" accept="image/*" hidden>
            </div>
            <button type="submit" id="submitBtn" disabled>Predict</button>
        </form>
        <div id="previewContainer" class="hidden">
            <img id="preview" src="#" alt="Preview">
        </div>

        <script>
            const dropZone = document.getElementById('dropZone');
            const fileInput = document.getElementById('fileInput');
            const submitBtn = document.getElementById('submitBtn');
            const previewContainer = document.getElementById('previewContainer');
            const preview = document.getElementById('preview');

            // Drag and drop handlers
            dropZone.addEventListener('click', () => fileInput.click());
            
            dropZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropZone.classList.add('dragover');
            });

            dropZone.addEventListener('dragleave', () => {
                dropZone.classList.remove('dragover');
            });

            dropZone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropZone.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length) {
                    fileInput.files = files;
                    handleFile(files[0]);
                }
            });

            // File input change handler
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length) {
                    handleFile(e.target.files[0]);
                }
            });

            // Handle selected file
            function handleFile(file) {
                if (file.type.startsWith('image/')) {
                    submitBtn.disabled = false;
                    previewContainer.classList.remove('hidden');
                    preview.src = URL.createObjectURL(file);
                } else {
                    alert('Пожалуйста, выберите изображение!');
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/predict/", response_class=HTMLResponse)
async def predict(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    input_path = save_uploaded_file(file, file_id)
    output_path = predict_image(model, input_path)
    download_link = output_path.split('/')[-1]

    return f"""
    <html>
    <body>
        <h2>Результат распознавания</h2>
        <img src="/{output_path}" style="max-width: 80%;">
        <div style="margin: 1rem 0;">
            <a href="/static/{download_link}" download>
                <button>Скачать результат</button>
            </a>
            <a href="/"><button>Назад</button></a>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    ngrok_token = input("Enter your ngrok authtoken: ").strip()
    if not ngrok_token:
        raise ValueError("Ngrok authtoken required!")
    
    conf.get_default().auth_token = ngrok_token
    nest_asyncio.apply()
    
    try:
        public_url = ngrok.connect(8000)
        print("Public URL:", public_url)
        uvicorn.run(app, port=8000)
    except Exception as e:
        print(f"Ngrok error: {e}")
        print("Check your authtoken: https://dashboard.ngrok.com/get-started/your-authtoken")
