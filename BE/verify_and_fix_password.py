"""
Verify và fix password hash cho user admin
"""
import bcrypt
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

def verify_and_fix():
    """Kiểm tra và fix password"""
    engine = create_engine(SQL_SERVER_PERMISSION_CONN)
    
    print("="*70)
    print("🔐 VERIFY & FIX PASSWORD")
    print("="*70)
    
    # Hash từ SQL script
    sql_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWEgEjqK"
    test_password = "admin123"
    
    print(f"\n1️⃣ Test hash từ SQL script...")
    print(f"   Hash: {sql_hash}")
    print(f"   Password: {test_password}")
    
    try:
        is_valid = bcrypt.checkpw(test_password.encode('utf-8'), sql_hash.encode('utf-8'))
        if is_valid:
            print("   ✅ Hash trong SQL script ĐÚNG với 'admin123'")
        else:
            print("   ❌ Hash trong SQL script KHÔNG KHỚP với 'admin123'")
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")
    
    print(f"\n2️⃣ Tạo hash mới cho 'admin123'...")
    new_hash = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    print(f"   New hash: {new_hash}")
    
    # Verify new hash
    is_valid_new = bcrypt.checkpw(test_password.encode('utf-8'), new_hash.encode('utf-8'))
    print(f"   Verify new hash: {'✅ ĐÚNG' if is_valid_new else '❌ SAI'}")
    
    print(f"\n3️⃣ Kiểm tra database...")
    with engine.connect() as conn:
        with conn.begin():
            # Check user admin
            check_sql = text("SELECT UserID, Username, PasswordHash, Status FROM [USER] WHERE Username = :username")
            result = conn.execute(check_sql, {"username": "admin"}).fetchone()
            
            if not result:
                print("   ❌ User 'admin' không tồn tại!")
                print("\n4️⃣ Tạo user admin mới...")
                
                insert_sql = text("""
                    INSERT INTO [USER] (Username, PasswordHash, Email, Status, EmailVerified)
                    VALUES (:username, :password, :email, :status, :verified)
                """)
                
                conn.execute(insert_sql, {
                    "username": "admin",
                    "password": new_hash,
                    "email": "admin@company.com",
                    "status": "ACTIVE",
                    "verified": 1
                })
                
                print("   ✅ Đã tạo user admin với password hash mới!")
                
            else:
                print(f"   ✅ User admin tồn tại (UserID: {result[0]})")
                print(f"   Status: {result[3]}")
                
                db_hash = result[2]
                print(f"\n4️⃣ So sánh hash trong database...")
                print(f"   DB hash: {db_hash[:50]}...")
                
                # Test hash trong database
                try:
                    is_valid_db = bcrypt.checkpw(test_password.encode('utf-8'), db_hash.encode('utf-8'))
                    if is_valid_db:
                        print("   ✅ Hash trong database ĐÚNG với 'admin123'")
                        print("\n" + "="*70)
                        print("🎉 PASSWORD ĐÃ ĐÚNG - LOGIN SẼ HOẠT ĐỘNG!")
                        print("="*70)
                    else:
                        print("   ❌ Hash trong database KHÔNG KHỚP với 'admin123'")
                        print("\n5️⃣ Cập nhật password hash mới...")
                        
                        update_sql = text("UPDATE [USER] SET PasswordHash = :password WHERE Username = :username")
                        conn.execute(update_sql, {
                            "password": new_hash,
                            "username": "admin"
                        })
                        
                        print("   ✅ Đã cập nhật password hash mới!")
                        print("\n" + "="*70)
                        print("🎉 PASSWORD ĐÃ ĐƯỢC FIX!")
                        print("="*70)
                        
                except Exception as e:
                    print(f"   ❌ Lỗi verify: {e}")
                    print("\n5️⃣ Cập nhật password hash mới...")
                    
                    update_sql = text("UPDATE [USER] SET PasswordHash = :password WHERE Username = :username")
                    conn.execute(update_sql, {
                        "password": new_hash,
                        "username": "admin"
                    })
                    
                    print("   ✅ Đã cập nhật password hash mới!")
                    print("\n" + "="*70)
                    print("🎉 PASSWORD ĐÃ ĐƯỢC FIX!")
                    print("="*70)
    
    print("\n📝 Thông tin đăng nhập:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n🔄 Hãy RESTART backend server và thử login lại!")
    print("="*70)

if __name__ == "__main__":
    try:
        verify_and_fix()
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
