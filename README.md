#  Англи Хэл Суралцах Систем - English Learning System

##  Багийн гишүүд
- **Таны нэр** - Full Stack хөгжүүлэгч
- **GitHub**: [github.com/username](https://github.com/username)
- **Утас**: +976-XXXX-XXXX

##  Товч танилцуулга
Англи хэл суралцах систем нь 6-12 насны хүүхдүүдэд зориулсан интерактив суралцах платформ юм. Энэхүү систем нь дасгал хийх, ахиц хянах, badge цуглуулах зэрэг функцуудыг агуулна.

### Гол функцууд
-  Хэрэглэгчийн бүртгэл ба нэвтрэх (JWT authentication)
-  Дөрвөн төрлийн дасгал (үсэг, унших, сонсох, бичих)
-  Ахиц хянах dashboard
-  Оноо цуглуулах систем
-  Badge шагнал олгох
-  Файл хуулах (audio, зураг)
-  Багш/Админ панел

##  Технологийн стек

### Backend
- **Python 3.11+**
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Өгөгдлийн сан
- **Pydantic** - Data validation
- **Bcrypt** - Password hashing
- **JWT** - Authentication

### Frontend
- **React 18** - UI library
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **Fetch API** - HTTP requests

##  Суулгах заавар

### Шаардлагатай зүйлс
```bash
# Backend
- Python 3.11 эсвэл түүнээс дээш
- PostgreSQL 14+
- pip package manager

# Frontend
- Node.js 18+
- npm эсвэл yarn
```

### 1. Repository clone хийх
```bash
git clone https://github.com/username/english-learning-system.git
cd english-learning-system
```

### 2. Backend суулгах

#### 2.1 Virtual environment үүсгэх
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

#### 2.2 Dependencies суулгах
```bash
pip install -r requirements.txt
```

#### 2.3 PostgreSQL өгөгдлийн сан үүсгэх
```sql
-- PostgreSQL дээр дараах командуудыг ажиллуулах
CREATE DATABASE english_learning;
CREATE USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE english_learning TO postgres;
```

#### 2.4 Database тохиргоо (database.py)
```python
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/english_learning"
```

#### 2.5 Database schema үүсгэх
```bash
python -c "from database import create_tables; create_tables()"
```

#### 2.6 Backend сервер ажиллуулах
```bash
python main.py
# Эсвэл
uvicorn main:app --reload --port 8001
```

### 3. Frontend суулгах

#### 3.1 Dependencies суулгах
```bash
cd frontend
npm install
```

#### 3.2 Frontend сервер ажиллуулах
```bash
npm start
```

Frontend: http://localhost:3000
Backend API: http://localhost:8001
API Docs: http://localhost:8001/docs

##  Ашиглах заавар

### Админ хэрэглэгч

#### Админ үүсгэх
```python
# backend folder дотор
python create_admin.py
# Username: admin1
# Password: admin123
```

#### Админ функцууд
- `/admin/login` - Нэвтрэх
- `/admin/dashboard` - Удирдлагын самбар
- `/upload` - Файл хуулах (audio, зураг)
- Сурагч болон багшийн мэдээллийг харах

### Багш хэрэглэгч

#### Бүртгүүлэх
1. Бүртгүүлэх хуудас руу орох
2. "Багш" сонгох
3. И-мэйл оруулах
4. Бүртгүүлэх

#### Багшийн функцууд
- Сурагчдынхаа ахицыг харах
- Дасгал үүсгэх (ирээдүйд)
- Файл хуулах

### Сурагч хэрэглэгч

#### Бүртгүүлэх
1. Бүртгүүлэх хуудас руу орох
2. "Сурагч" сонгох
3. Нас оруулах (5-15)
4. Бүртгүүлэх

#### Сурагчийн функцууд
- **Үсэг сургах** - A-Z үсгийг сурах
- **Унших дасгал** - Өгүүлбэр уншиж суралцах
- **Сонсох дасгал** - Аудио сонсож үг таних
- **Бичих дасгал** - Үг бичиж дадлага хийх
- **Миний ахиц** - Оноо, амжилт харах

### Оноо систем
- Зөв хариулт = +10 оноо
- Буруу хариулт = 0 оноо
- 100 оноо = "Star Reader" badge
- 200 оноо = "Master Reader" badge

##  Файлын бүтэц

```
english-learning-system/
│
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── database.py             # Database connection
│   ├── models.py               # SQLAlchemy models
│   ├── requirements.txt        # Python dependencies
│   ├── uploads/                # Uploaded files
│   │   ├── audio/
│   │   └── images/
│   └── venv/                   # Virtual environment
│
├── frontend/
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   ├── components/
│   │   │   ├── LoginPage.js
│   │   │   ├── RegisterPage.js
│   │   │   ├── StudentHomePage.js
│   │   │   ├── ExercisePage.js
│   │   │   ├── ProgressPage.js
│   │   │   └── Dashboard.js
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
│
├── FINALREADME.md
└── PROJECT_REPORT.md
```

##  Түгээмэл асуултууд (FAQ)

### Q: Нууц үгээ мартсан бол?
A: Одоогоор password reset функц байхгүй. Админаас хандаж нууц үгээ шинэчлүүлнэ үү.

### Q: Дасгал олдохгүй байна?
A: Database-д дасгал үүсгэх хэрэгтэй. Demo дасгалууд автоматаар харагдана.

### Q: Progress хадгалагдахгүй байна?
A: 
1. Backend сервер ажиллаж байгаа эсэхийг шалгана уу
2. Database холболт зөв эсэхийг шалгана уу
3. Student record үүссэн эсэхийг шалгана уу

### Q: Файл хуулахад алдаа гарна?
A: 
- Зургийн хэмжээ: < 5MB
- Аудио файлын хэмжээ: < 10MB
- Зөвшөөрөгдсөн өргөтгөл: .jpg, .png, .mp3, .wav

### Q: Mobile дээр ашиглаж болох уу?
A: Одоогоор desktop дээр сайн харагдана. Mobile responsive дэмжлэг удахгүй нэмэгдэнэ.

##  Хөгжүүлэлтийн горим (Development)

### Backend development
```bash
cd backend
python main.py
# Hot reload enabled
```

### Frontend development
```bash
cd frontend
npm start
# Hot reload enabled
```

### Database migration
```bash
# Шинэ багана нэмэх
alembic revision --autogenerate -m "Add column"
alembic upgrade head
```

##  Testing

### Backend tests (Ирээдүйд)
```bash
pytest tests/
```

### Frontend tests (Ирээдүйд)
```bash
npm test
```

##  Production deployment

### Docker ашиглах
```bash
# Backend
docker build -t english-backend ./backend
docker run -p 8001:8001 english-backend

# Frontend
docker build -t english-frontend ./frontend
docker run -p 3000:3000 english-frontend
```

### Environment Variables
```bash
# .env файл үүсгэх
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/dbname
ALLOWED_ORIGINS=http://localhost:3000
```

##  Аюулгүй байдал

### Хэрэгжүүлсэн арга хэмжээ
-  JWT token authentication
-  Password bcrypt hashing
-  SQL injection сэргийлэлт (SQLAlchemy ORM)
-  Input validation (Pydantic)
-  CORS policy (одоогоор allow_all)

### Сайжруулах шаардлагатай
-  Rate limiting
-  CSRF protection
-  XSS protection headers
- HTTPS
- Password reset mechanism

##  Алдаа засварлах (Troubleshooting)

### Backend алдаа
```bash
# Module import алдаа
pip install -r requirements.txt

# Database холболт алдаа
# PostgreSQL ажиллаж байгаа эсэхийг шалгах
psql -U postgres -d english_learning

# Port эзлэгдсэн
# Process-ийг таслах (Windows)
netstat -ano | findstr :8001
taskkill /PID <process_id> /F
```

### Frontend алдаа
```bash
# Node modules алдаа
rm -rf node_modules
npm install

# Port эзлэгдсэн
# .env файлд PORT=3001 гэж өөрчлөх
```


##  License

MIT License - Энэхүү төсөл нь судалгааны зорилгоор хийгдсэн.


**Анхааруулга**: Энэхүү систем нь сургалтын зорилгоор хийгдсэн бөгөөд production орчинд ашиглахаас өмнө аюулгүй байдлын нэмэлт арга хэмжээ авах шаардлагатай.

**Хувилбар**: 1.0.0  
**Огноо**: 2025 оны 12-р сар  
**Статус**:  Development Complete
