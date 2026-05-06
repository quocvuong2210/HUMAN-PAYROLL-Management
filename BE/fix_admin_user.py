"""
Fix user admin - Đổi username 'a' về 'admin' và Status về 'ACTIVE'
"""
import bcrypt
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

def fix_admin_user():
    """Fix user admin"""
    engine = create_engine(SQL_SERVER_PERMISSION_CONN)
    
    print("="*70)
    print("🔧 FIX USER ADMIN")
    print("="*70)
    
    with engine.connect() as conn:
        with conn.begin():
            # 1. Kiểm tra user 'a'
            print("\n1️⃣ Kiểm tra user 'a'...")
            check_sql = text("SELECT UserID, Username, Status FROM [USER] WHERE Username = :username")
            result = conn.execute(check_sql, {"username": "a"}).fetchone()
            
            if result:
                user_id = result[0]
                username = result[1]
                status = result[2]
                
                print(f"   ✅ Tìm thấy user 'a'")
                print(f"      UserID: {user_id}")
                print(f"      Username: {username}")
                print(f"      Status: {status}")
                
                # 2. Fix username và status
                print(f"\n2️⃣ Đang fix...")
                
                # Tạo password hash mới cho admin123
                password_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                update_sql = text("""
                    UPDATE [USER]
                    SET Username = :new_username,
                        Status = :new_status,
                        PasswordHash = :password
                    WHERE UserID = :user_id
                """)
                
                conn.execute(update_sql, {
                    "new_username": "admin",
                    "new_status": "ACTIVE",
                    "password": password_hash,
                    "user_id": user_id
                })
                
                print(f"   ✅ Đã cập nhật:")
                print(f"      Username: 'a' → 'admin'")
                print(f"      Status: '{status}' → 'ACTIVE'")
                print(f"      Password: Đã reset về 'admin123'")
                
            else:
                print(f"   ❌ Không tìm thấy user 'a'")
                
                # Kiểm tra xem có user admin không
                admin_check = conn.execute(check_sql, {"username": "admin"}).fetchone()
                
                if admin_check:
                    print(f"\n   ✅ User 'admin' đã tồn tại")
                    print(f"      Chỉ cần fix status và password...")
                    
                    password_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    
                    update_sql = text("""
                        UPDATE [USER]
                        SET Status = :new_status,
                            PasswordHash = :password
                        WHERE Username = :username
                    """)
                    
                    conn.execute(update_sql, {
                        "new_status": "ACTIVE",
                        "password": password_hash,
                        "username": "admin"
                    })
                    
                    print(f"   ✅ Đã cập nhật user 'admin'")
                else:
                    print(f"\n   ❌ Không có user 'admin' hoặc 'a'")
                    print(f"   → Cần tạo user admin mới")
                    return
            
            # 3. Verify
            print(f"\n3️⃣ Verify...")
            verify_sql = text("SELECT UserID, Username, Status FROM [USER] WHERE Username = :username")
            verify_result = conn.execute(verify_sql, {"username": "admin"}).fetchone()
            
            if verify_result:
                print(f"   ✅ User 'admin' đã OK")
                print(f"      UserID: {verify_result[0]}")
                print(f"      Username: {verify_result[1]}")
                print(f"      Status: {verify_result[2]}")
            else:
                print(f"   ❌ Verify thất bại!")
                return
    
    print("\n" + "="*70)
    print("🎉 FIX THÀNH CÔNG!")
    print("="*70)
    print("\n📝 Thông tin đăng nhập:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n🔄 Hãy RESTART backend và thử login lại!")
    print("="*70)

if __name__ == "__main__":
    try:
        fix_admin_user()
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
