
# === Database холболт ===
# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
    

# PostgreSQL холболтын тохиргоо
DATABASE_URL = "postgresql://odoo:odoo123@localhost:5432/english_learning_db"
# SQLite ашиглах бол (PostgreSQL суулгаагүй үед):
# DATABASE_URL = "sqlite:///./english_learning.db"

# Engine үүсгэх
engine = create_engine(
    DATABASE_URL,
    # SQLite бол uncomment хийх:
    # connect_args={"check_same_thread": False}
)

# Session үүсгэх
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class үүсгэх
Base = declarative_base()

# Database session авах функц
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database table үүсгэх функц
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables үүссэн!")

# Database table устгах функц (dev орчинд)
def drop_tables():
    Base.metadata.drop_all(bind=engine)
    print(" Database tables устгагдлаа!")