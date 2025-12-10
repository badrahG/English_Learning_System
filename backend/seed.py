# seed.py - Анхны өгөгдөл оруулах

from database import SessionLocal, create_tables
from models import User, Student, Teacher, Exercise, Badge
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_database():
    """Анхны өгөгдлийг database-д оруулах"""
    
    # Database tables үүсгэх
    create_tables()
    
    db = SessionLocal()
    
    try:
        # ========================================
        # 1. ХЭРЭГЛЭГЧИД ҮҮСГЭХ
        # ========================================
        
        print(" Хэрэглэгчид үүсгэж байна...")
        
        # Сурагч 1
        user1 = User(
            username="student1",
            password_hash=pwd_context.hash("pass123"),
            name="Болд",
            role="student",
            age=7,
            email=None
        )
        db.add(user1)
        db.flush()  # ID авах
        
        # Сурагч 2
        user2 = User(
            username="student2",
            password_hash=pwd_context.hash("pass123"),
            name="Сарнай",
            role="student",
            age=6,
            email=None
        )
        db.add(user2)
        db.flush()
        
        # Багш 1
        user3 = User(
            username="teacher1",
            password_hash=pwd_context.hash("pass123"),
            name="Багш Оюунаа",
            role="teacher",
            age=None,
            email="teacher@example.com"
        )
        db.add(user3)
        db.flush()
        
        # Админ 1
        user4 = User(
            username="admin1",
            password_hash=pwd_context.hash("pass123"),
            name="Админ",
            role="admin",
            age=None,
            email="admin@example.com"
        )
        db.add(user4)
        db.flush()
        
        print(f" {db.query(User).count()} хэрэглэгч үүслээ")
        
        # ========================================
        # 2. СУРАГЧДЫН МЭДЭЭЛЭЛ
        # ========================================
        
        print(" Сурагчдын мэдээлэл үүсгэж байна...")
        
        student1 = Student(
            user_id=user1.id,
            name="Болд",
            age=7,
            level="Beginner",
            total_score=120,
            badges=["Alphabet Hero", "Star Reader"]
        )
        db.add(student1)
        
        student2 = Student(
            user_id=user2.id,
            name="Сарнай",
            age=6,
            level="Beginner",
            total_score=85,
            badges=["Alphabet Hero"]
        )
        db.add(student2)
        
        print(f" {db.query(Student).count()} сурагч үүслээ")
        
        # ========================================
        # 3. БАГШИЙН МЭДЭЭЛЭЛ
        # ========================================
        
        print(" Багшийн мэдээлэл үүсгэж байна...")
        
        teacher1 = Teacher(
            user_id=user3.id,
            name="Багш Оюунаа",
            email="teacher@example.com"
        )
        db.add(teacher1)
        
        print(f" {db.query(Teacher).count()} багш үүслээ")
        
        # ========================================
        # 4. ДАСГАЛУУД
        # ========================================
        
        print(" Дасгалууд үүсгэж байна...")
        
        exercises = [
            # Үсэг сургах
            Exercise(
                type="letter",
                level="Beginner",
                question="A үсэг ямар дуутай эхэлдэг вэ?",
                options=["Apple", "Banana", "Cat", "Dog"],
                correct_answer="Apple",
                audio_url="/uploads/audio/letter_a.mp3",
                image_url="/uploads/images/apple.png",
                points=10
            ),
            Exercise(
                type="letter",
                level="Beginner",
                question="B үсэг ямар дуутай эхэлдэг вэ?",
                options=["Apple", "Banana", "Cat", "Dog"],
                correct_answer="Banana",
                audio_url="/uploads/audio/letter_b.mp3",
                image_url="/uploads/images/banana.png",
                points=10
            ),
            
            # Унших дасгал
            Exercise(
                type="reading",
                level="Beginner",
                question="Уншаад зөв хариуг сонго: 'The cat is on the table.'",
                options=["Муур ширээн дээр байна", "Нохой сандал доор байна", "Шувуу модон дээр байна"],
                correct_answer="Муур ширээн дээр байна",
                audio_url=None,
                image_url=None,
                points=10
            ),
            Exercise(
                type="reading",
                level="Beginner",
                question="Уншаад зөв хариуг сонго: 'The dog is under the chair.'",
                options=["Муур ширээн дээр байна", "Нохой сандал доор байна", "Шувуу модон дээр байна"],
                correct_answer="Нохой сандал доор байна",
                audio_url=None,
                image_url=None,
                points=10
            ),
            
            # Сонсох дасгал
            Exercise(
                type="listening",
                level="Beginner",
                question="Сонсоод зөв үгийг сонго",
                options=["Apple", "Banana", "Cat"],
                correct_answer="Apple",
                audio_url="/uploads/audio/word_apple.mp3",
                image_url=None,
                points=10
            ),
            Exercise(
                type="listening",
                level="Beginner",
                question="Сонсоод зөв үгийг сонго",
                options=["Dog", "Bird", "Fish"],
                correct_answer="Dog",
                audio_url="/uploads/audio/word_dog.mp3",
                image_url=None,
                points=10
            ),
            
            # Бичих дасгал
            Exercise(
                type="writing",
                level="Beginner",
                question="Сонссон үгээ бич",
                options=[],
                correct_answer="dog",
                audio_url="/uploads/audio/word_dog.mp3",
                image_url=None,
                points=10
            ),
            Exercise(
                type="writing",
                level="Beginner",
                question="Сонссон үгээ бич",
                options=[],
                correct_answer="cat",
                audio_url="/uploads/audio/word_cat.mp3",
                image_url=None,
                points=10
            ),
        ]
        
        for ex in exercises:
            db.add(ex)
        
        print(f" {len(exercises)} дасгал үүслээ")
        
        # ========================================
        # 5. BADGE-УУД
        # ========================================
        
        print(" Badge-ууд үүсгэж байна...")
        
        badges = [
            Badge(
                name="Alphabet Hero",
                description="26 үсгийг амжилттай дүүргэсэн",
                icon="🔤",
                required_score=50
            ),
            Badge(
                name="Star Reader",
                description="100 оноонд хүрсэн",
                icon="⭐",
                required_score=100
            ),
            Badge(
                name="Master Reader",
                description="200 оноонд хүрсэн",
                icon="🏆",
                required_score=200
            ),
            Badge(
                name="Listening Pro",
                description="Сонсох дасгалыг 50 удаа хийсэн",
                icon="👂",
                required_score=150
            ),
            Badge(
                name="Writing Expert",
                description="Бичих дасгалыг 50 удаа хийсэн",
                icon="✍️",
                required_score=150
            ),
        ]
        
        for badge in badges:
            db.add(badge)
        
        print(f"✅ {len(badges)} badge үүслээ")
        
        # ========================================
        # COMMIT
        # ========================================
        
        db.commit()
        print("\n Бүх өгөгдөл амжилттай оруулагдлаа!\n")
        
        # Хураангуй
        print("=" * 50)
        print(" ХУРААНГУЙ:")
        print("=" * 50)
        print(f"👥 Хэрэглэгч: {db.query(User).count()}")
        print(f"👨‍🎓 Сурагч: {db.query(Student).count()}")
        print(f"👨‍🏫 Багш: {db.query(Teacher).count()}")
        print(f"📝 Дасгал: {db.query(Exercise).count()}")
        print(f"🏆 Badge: {db.query(Badge).count()}")
        print("=" * 50)
        print("\n seed.py амжилттай дууслаа!")
        print("\n Тест хэрэглэгчид:")
        print("   - student1 / pass123")
        print("   - student2 / pass123")
        print("   - teacher1 / pass123")
        print("   - admin1 / pass123")
        
    except Exception as e:
        print(f"\n АЛДАА: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print(" АНХНЫ ӨГӨГДӨЛ ОРУУЛЖ БАЙНА...")
    print("=" * 50 + "\n")
    seed_database()