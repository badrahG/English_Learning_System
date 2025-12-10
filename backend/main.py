# main.py - FastAPI with SQLAlchemy Database (БҮРЭН ХУВИЛБАР)

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
import uvicorn
import os
import shutil

# Local imports
from database import get_db, create_tables
from models import User, Student, Teacher, Exercise, Progress, Badge, UploadedFile

# ========================================
# ТОХИРГОО
# ========================================

SECRET_KEY = "9f2e9e3c1c4a57d0e3b6b4f87a23dcffb7918df5c8143bab03c7c9f648be39d1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 өдөр

# Файл хадгалах folder
UPLOAD_DIR = "uploads"
AUDIO_DIR = os.path.join(UPLOAD_DIR, "audio")
IMAGE_DIR = os.path.join(UPLOAD_DIR, "images")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# ========================================
# FASTAPI APP
# ========================================

app = FastAPI(title="English Learning System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Database tables үүсгэх
create_tables()

# ========================================
# PYDANTIC MODELS
# ========================================

# Authentication Models
class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    role: str  # student, teacher, admin
    age: Optional[int] = None
    email: Optional[EmailStr] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

# Exercise Models
class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    level: str = "Beginner"
    total_score: int = 0
    badges: List[str] = []
    
    class Config:
        from_attributes = True

class ExerciseResponse(BaseModel):
    id: int
    type: str
    question: str
    options: List[str]
    correct_answer: str
    audio_url: Optional[str] = None
    image_url: Optional[str] = None
    
    class Config:
        from_attributes = True

class ProgressResponse(BaseModel):
    student_id: int
    exercise_id: int
    is_correct: bool
    score: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# ========================================
# HELPER FUNCTIONS
# ========================================

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Токен буруу байна",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# ========================================
# AUTHENTICATION ENDPOINTS
# ========================================

@app.post("/auth/register", response_model=dict)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Хэрэглэгч давхцаж байгаа эсэхийг шалгах
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Хэрэглэгчийн нэр аль хэдийн бүртгэгдсэн байна"
        )
    
    # Шинэ хэрэглэгч үүсгэх
    new_user = User(
        username=user.username,
        password_hash=get_password_hash(user.password),
        name=user.name,
        role=user.role,
        age=user.age,
        email=user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Хэрэв сурагч бол student table-д нэмэх
    if user.role == "student":
        new_student = Student(
            user_id=new_user.id,
            name=user.name,
            age=user.age or 7,
            level="Beginner",
            total_score=0,
            badges=[]
        )
        db.add(new_student)
        db.commit()
    
    # Хэрэв багш бол teacher table-д нэмэх
    if user.role == "teacher":
        new_teacher = Teacher(
            user_id=new_user.id,
            name=user.name,
            email=user.email
        )
        db.add(new_teacher)
        db.commit()
    
    return {
        "message": "Амжилттай бүртгүүллээ",
        "user": {
            "username": new_user.username,
            "name": new_user.name,
            "role": new_user.role
        }
    }

@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Хэрэглэгчийн нэр эсвэл нууц үг буруу байна",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "role": user.role,
            "age": user.age,
            "email": user.email
        }
    }

@app.get("/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "name": current_user.name,
        "role": current_user.role,
        "age": current_user.age,
        "email": current_user.email
    }

# ========================================
# FILE UPLOAD ENDPOINTS
# ========================================

@app.post("/upload/file")
async def upload_file(
    file: UploadFile = File(...),
    file_type: str = "image",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Танд файл хуулах эрх байхгүй байна"
        )
    
    if file_type not in ["audio", "image"]:
        raise HTTPException(status_code=400, detail="Файлын төрөл буруу байна")
    
    allowed_extensions = {
        "audio": [".mp3", ".wav", ".ogg", ".m4a"],
        "image": [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    }
    
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions[file_type]:
        raise HTTPException(
            status_code=400,
            detail=f"Зөвшөөрөгдсөн өргөтгөл: {', '.join(allowed_extensions[file_type])}"
        )
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    
    if file_type == "audio":
        file_path = os.path.join(AUDIO_DIR, safe_filename)
    else:
        file_path = os.path.join(IMAGE_DIR, safe_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Файл хадгалахад алдаа гарлаа: {str(e)}")
    
    # Database-д хадгалах
    uploaded_file = UploadedFile(
        filename=safe_filename,
        original_filename=file.filename,
        file_path=file_path,
        file_type=file_type,
        size=os.path.getsize(file_path),
        uploaded_by=current_user.id
    )
    db.add(uploaded_file)
    db.commit()
    
    return {
        "filename": safe_filename,
        "file_path": f"/uploads/{file_type}/{safe_filename}",
        "file_type": file_type,
        "size": uploaded_file.size
    }

@app.get("/upload/files")
async def get_uploaded_files(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role in ["teacher", "admin"]:
        files = db.query(UploadedFile).all()
    else:
        files = db.query(UploadedFile).filter(UploadedFile.uploaded_by == current_user.id).all()
    
    return {
        "files": [
            {
                "id": f.id,
                "name": f.original_filename,
                "type": f.file_type,
                "size": f"{round(f.size / 1024, 2)} KB",
                "url": f"/uploads/{f.file_type}/{f.filename}"
            }
            for f in files
        ]
    }

@app.delete("/upload/file/{file_id}")
async def delete_file(file_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Танд файл устгах эрх байхгүй байна")
    
    file_info = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
    if not file_info:
        raise HTTPException(status_code=404, detail="Файл олдсонгүй")
    
    try:
        os.remove(file_info.file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Файл устгахад алдаа гарлаа: {str(e)}")
    
    db.delete(file_info)
    db.commit()
    return {"message": "Файл амжилттай устгагдлаа"}

# ========================================
# EXERCISE ENDPOINTS
# ========================================

@app.get("/")
def root():
    return {
        "message": "English Learning System API",
        "version": "2.0",
        "features": ["Authentication", "File Upload", "Exercises", "Database"]
    }

@app.get("/students", response_model=List[StudentResponse])
async def get_students(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role in ["teacher", "admin"]:
        students = db.query(Student).all()
        return students
    
    # Сурагч зөвхөн өөрийн мэдээллийг харна
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    return [student] if student else []

@app.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Сурагч олдсонгүй")
    
    # Эрх шалгах
    if current_user.role == "student" and student.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Танд хандах эрх байхгүй байна")
    
    return student

@app.get("/exercises", response_model=List[ExerciseResponse])
def get_exercises(db: Session = Depends(get_db)):
    exercises = db.query(Exercise).all()
    return exercises

@app.get("/exercises/type/{exercise_type}", response_model=List[ExerciseResponse])
def get_exercises_by_type(exercise_type: str, db: Session = Depends(get_db)):
    exercises = db.query(Exercise).filter(Exercise.type == exercise_type).all()
    if not exercises:
        raise HTTPException(status_code=404, detail="Дасгал олдсонгүй")
    return exercises

@app.post("/submit-answer")
def submit_answer(
    student_id: int,
    exercise_id: int,
    user_answer: str,
    db: Session = Depends(get_db)
):
    # Дасгал олох
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Дасгал олдсонгүй")
    
    # Хариу шалгах
    is_correct = user_answer.lower().strip() == exercise.correct_answer.lower().strip()
    score = 10 if is_correct else 0
    
    # Ахиц хадгалах (DATABASE-д)
    progress_entry = Progress(
        student_id=student_id,
        exercise_id=exercise_id,
        is_correct=is_correct,
        score=score,
        user_answer=user_answer
    )
    db.add(progress_entry)
    
    # Сурагчийн нийт оноог шинэчлэх
    student = db.query(Student).filter(Student.id == student_id).first()
    if student:
        student.total_score += score
        
        # Badge олгох
        if student.total_score >= 100 and "Star Reader" not in student.badges:
            student.badges = student.badges + ["Star Reader"]
        
        if student.total_score >= 200 and "Master Reader" not in student.badges:
            student.badges = student.badges + ["Master Reader"]
    
    db.commit()
    
    return {
        "is_correct": is_correct,
        "score": score,
        "total_score": student.total_score if student else 0,
        "message": "Маш сайн!" if is_correct else "Дахиад оролдоорой!"
    }

@app.get("/progress/{student_id}")
def get_progress(student_id: int, db: Session = Depends(get_db)):
    # Database-аас progress авах
    student_progress = db.query(Progress).filter(Progress.student_id == student_id).all()
    
    if not student_progress:
        return {
            "student_id": student_id,
            "total_exercises": 0,
            "correct_answers": 0,
            "accuracy": 0,
            "total_score": 0
        }
    
    total = len(student_progress)
    correct = sum(1 for p in student_progress if p.is_correct)
    accuracy = round((correct / total) * 100, 2) if total > 0 else 0
    total_score = sum(p.score for p in student_progress)
    
    return {
        "student_id": student_id,
        "total_exercises": total,
        "correct_answers": correct,
        "accuracy": accuracy,
        "total_score": total_score
    }

@app.get("/badges/{student_id}")
def get_badges(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Сурагч олдсонгүй")
    
    return {
        "student_id": student_id,
        "badges": student.badges,
        "total_badges": len(student.badges)
    }

# ========================================
# SERVER
# ========================================

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)