"""
Script kiểm tra user admin trong database
"""
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN
import bcrypt

def check_admin_user():
    """Kiểm tra user admin có tồn tại không và password hash"""
    engine = create_engine(SQL_SERVER_PERMISSION_CONN)
    
    with engine.connect() as conn:
        # Kiểm tra user admin
        check_sql = text("SELECT UserID, Username, PasswordHash, Email, Status, EmailVerified FROM [USER] WHERE Username = :username")
        result = conn.execute(check_sql, {"username": "admin"}).fetchone()
        
        if not result:
            print("❌ User 'admin' KHÔNG tồn tại trong database")
            print("\n📝 Hãy chạy: python BE/create_admin_user.py")
            return
        
        print("✅ User 'admin' tồn tại trong database")
        print(f"   UserID: {result[0]}")
        print(f"   Username: {result[1]}")
        print(f"   Email: {result[3]}")
        print(f"   Status: {result[4]}")
        print(f"   EmailVerified: {result[5]}")
        print(f"   PasswordHash: {result[2][:50]}...")
        
        # Test password
        password_hash = result[2]
        test_password = "admin123"
        
        try:
            if bcrypt.checkpw(test_password.encode('utf-8'), password_hash.encode('utf-8')):
                print(f"\n✅ Password 'admin123' ĐÚNG với hash trong database")
            else:
                print(f"\n❌ Password 'admin123' KHÔNG KHỚP với hash trong database")
        except Exception as e:
            print(f"\n❌ Lỗi kiểm tra password: {e}")
            print(f"   Hash format có thể không đúng bcrypt")

if __name__ == "__main__":
    try:
        check_admin_user()
    except Exception as e:
        print(f"❌ Lỗi kết nối database: {e}")
