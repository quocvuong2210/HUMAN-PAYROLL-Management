"""
Script để reset passwords cho sample users
Chạy script này để tạo lại passwords với hash method đúng
"""
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash
from config import SQL_SERVER_PERMISSION_CONN

def reset_passwords():
    """Reset passwords cho tất cả sample users"""
    engine = create_engine(SQL_SERVER_PERMISSION_CONN)
    
    # Sample users với passwords
    users = [
        {"username": "admin", "password": "admin123"},
        {"username": "hr_manager", "password": "admin123"},
        {"username": "accountant", "password": "admin123"},
        {"username": "employee", "password": "admin123"}
    ]
    
    print("🔄 Đang reset passwords với method='pbkdf2:sha256'...")
    print("=" * 60)
    
    with engine.connect() as conn:
        with conn.begin():
            for user in users:
                # Hash password với method='pbkdf2:sha256'
                hashed_password = generate_password_hash(user['password'], method='pbkdf2:sha256')
                
                # Update password
                sql = text("""
                    UPDATE [USER]
                    SET [Password] = :password, [Status] = 'ACTIVE'
                    WHERE Username = :username
                """)
                
                result = conn.execute(sql, {
                    "password": hashed_password,
                    "username": user['username']
                })
                
                if result.rowcount > 0:
                    print(f"✅ Reset password cho user: {user['username']}")
                    print(f"   Hash: {hashed_password[:50]}...")
                else:
                    print(f"⚠️  User không tồn tại: {user['username']}")
    
    print("=" * 60)
    print("✅ Hoàn thành!")
    print("\nSample users:")
    print("  - admin / admin123 → SUPER_ADMIN")
    print("  - hr_manager / admin123 → HR_MANAGER")
    print("  - accountant / admin123 → PAYROLL_ACCOUNTANT")
    print("  - employee / admin123 → EMPLOYEE")
    print("\n⚠️  LƯU Ý: Tất cả passwords đã được hash với method='pbkdf2:sha256'")

if __name__ == "__main__":
    try:
        reset_passwords()
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()
