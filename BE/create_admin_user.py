"""
Script để tạo user admin nếu chưa có trong database
"""
import bcrypt
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

def create_admin_user():
    """Tạo user admin với password admin123"""
    engine = create_engine(SQL_SERVER_PERMISSION_CONN)
    
    # Hash password
    password = "admin123"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    with engine.connect() as conn:
        # Kiểm tra user admin đã tồn tại chưa
        check_sql = text("SELECT COUNT(*) as Count FROM [USER] WHERE Username = :username")
        result = conn.execute(check_sql, {"username": "admin"}).fetchone()
        
        if result[0] > 0:
            print("✅ User 'admin' đã tồn tại trong database")
            return
        
        # Tạo user admin mới
        insert_sql = text("""
            INSERT INTO [USER] (Username, PasswordHash, Email, Status, EmailVerified)
            VALUES (:username, :password, :email, :status, :verified)
        """)
        
        conn.execute(insert_sql, {
            "username": "admin",
            "password": hashed_password,
            "email": "admin@company.com",
            "status": "ACTIVE",
            "verified": 1
        })
        conn.commit()
        
        print("✅ Đã tạo user 'admin' thành công!")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Email: admin@company.com")

if __name__ == "__main__":
    try:
        create_admin_user()
    except Exception as e:
        print(f"❌ Lỗi: {e}")
