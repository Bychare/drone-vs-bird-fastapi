import os
import shutil

def save_uploaded_file(file, file_id):
    os.makedirs("static", exist_ok=True)
    input_path = f"static/{file_id}.jpg"
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return input_path
