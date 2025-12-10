# upload.py - File upload логик

from fastapi import HTTPException, UploadFile, File
from datetime import datetime
import os
import shutil

# Тохиргоо
UPLOAD_DIR = "uploads"
AUDIO_DIR = os.path.join(UPLOAD_DIR, "audio")
IMAGE_DIR = os.path.join(UPLOAD_DIR, "images")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# Database
uploaded_files_db = []

# File upload логик
async def save_file(file: UploadFile, file_type: str, user_id: int):
    # Өргөтгөл шалгах
    allowed_extensions = {
        "audio": [".mp3", ".wav", ".ogg", ".m4a"],
        "image": [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    }
    
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions[file_type]:
        raise HTTPException(400, detail=f"Invalid file type")
    
    # Файлын нэр үүсгэх
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    
    # Хадгалах зам
    if file_type == "audio":
        file_path = os.path.join(AUDIO_DIR, safe_filename)
    else:
        file_path = os.path.join(IMAGE_DIR, safe_filename)
    
    # Файл хадгалах
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Database-д хадгалах
    file_info = {
        "id": len(uploaded_files_db) + 1,
        "filename": safe_filename,
        "original_filename": file.filename,
        "file_path": file_path,
        "file_type": file_type,
        "size": os.path.getsize(file_path),
        "uploaded_by": user_id,
        "uploaded_at": datetime.now()
    }
    uploaded_files_db.append(file_info)
    
    return file_info

def get_files_by_user(user_id: int, user_role: str):
    if user_role in ["teacher", "admin"]:
        return uploaded_files_db
    return [f for f in uploaded_files_db if f["uploaded_by"] == user_id]