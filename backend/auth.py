# auth.py - Authentication логик
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr
from typing import Optional

# Тохиргоо
SECRET_KEY = "9f2e9e3c1c4a57d0e3b6b4f87a23dcffb7918df5c8143bab03c7c9f648be39d1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Database (in-memory)
users_db = []

# Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    role: str
    age: Optional[int] = None
    email: Optional[EmailStr] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

# Helper functions
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_username(username: str):
    return next((u for u in users_db if u["username"] == username), None)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user = get_user_by_username(username)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Анхны тест хэрэглэгчид
def init_test_users():
    test_users = [
        {
            "id": 1,
            "username": "student1",
            "password_hash": get_password_hash("pass123"),
            "name": "Болд",
            "role": "student",
            "age": 7,
            "created_at": datetime.now()
        },
        {
            "id": 2,
            "username": "teacher1",
            "password_hash": get_password_hash("pass123"),
            "name": "Багш Сарнай",
            "role": "teacher",
            "email": "teacher@example.com",
            "created_at": datetime.now()
        },
        {
            "id": 3,
            "username": "admin1",
            "password_hash": get_password_hash("pass123"),
            "name": "Админ",
            "role": "admin",
            "email": "admin@example.com",
            "created_at": datetime.now()
        }
    ]
    users_db.extend(test_users)

init_test_users()