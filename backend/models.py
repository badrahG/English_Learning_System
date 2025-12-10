# models.py - SQLAlchemy ORM Models

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# ========================================
# 1. User Model - Хэрэглэгч
# ========================================

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(20), default="student")  # student, teacher, admin
    age = Column(Integer, nullable=True)
    email = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="user", uselist=False)
    teacher = relationship("Teacher", back_populates="user", uselist=False)

# ========================================
# 2. Student Model - Сурагч
# ========================================

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    level = Column(String(20), default="Beginner")  # Beginner, Intermediate, Advanced
    total_score = Column(Integer, default=0)
    badges = Column(JSON, default=list)  # ["Alphabet Hero", "Star Reader"]
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="student")
    progress = relationship("Progress", back_populates="student", cascade="all, delete-orphan")

# ========================================
# 3. Teacher Model - Багш
# ========================================

class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="teacher")

# ========================================
# 4. Exercise Model - Дасгал
# ========================================

class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20), nullable=False, index=True)  # letter, reading, listening, writing
    level = Column(String(20), default="Beginner")
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=True)  # ["Apple", "Banana", "Cat"]
    correct_answer = Column(String(200), nullable=False)
    audio_url = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    points = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    progress = relationship("Progress", back_populates="exercise", cascade="all, delete-orphan")

# ========================================
# 5. Progress Model - Ахиц
# ========================================

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    score = Column(Integer, default=0)
    user_answer = Column(String(200), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="progress")
    exercise = relationship("Exercise", back_populates="progress")

# ========================================
# 6. Badge Model - Шагнал
# ========================================

class Badge(Base):
    __tablename__ = "badges"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(255), nullable=True)
    required_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

# ========================================
# 7. UploadedFile Model - Хуулсан файлууд
# ========================================

class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(20), nullable=False)  # audio, image
    size = Column(Integer, nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)