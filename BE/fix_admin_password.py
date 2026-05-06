"""
Script kiểm tra và fix password của user admin
"""
import bcrypt
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

def fix_admin_password():
    """Kiểm tra và fix password admin"""
    engine = create_engine(SQL_SERVER_PERMISSION_CONN)
    
    with engine.connect() as conn:
        with conn.begin():
            # 1. Kiểm tra user admin
            check_sql = text("SELECT UserID, Username, PasswordHash, Email, Status, EmailVerified FROM [USER] WHERE Username = :username")
            result = conn.execute(check_sql, {"username": "admin"}).fetchone()
            
            if not result:
                print("❌ User 'admin' KHÔNG tồn tại")
                print("\n📝 Tạo user admin mới...")
                
                # Tạo user admin
                password = "admin123"
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
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
                
                print("✅ Đã tạo user 'admin' thành công!")
                print(f"   Username: admin")
                print(f"   Password: admin123")
                print(f"   Email: admin@company.com")
                return
            
            # 2. User đã tồn tại - kiểm tra password
            print("✅ User 'admin' đã tồn tại")
            print(f"   UserID: {result[0]}")
            print(f"   Username: {result[1]}")
            print(f"   Email: {result[3]}")
            print(f"   Status: {result[4]}")
            print(f"   EmailVerified: {result[5]}")
            
            password_hash = result[2]
            print(f"   PasswordHash: {password_hash[:50]}...")
            
            # 3. Test password
            test_password = "admin123"
            
            try:
                if bcrypt.checkpw(test_password.encode('utf-8'), password_hash.encode('utf-8')):
                    print(f"\n✅ Password 'admin123' ĐÚNG!")
                    print("   → Login sẽ hoạt động bình thường")
                else:
                    print(f"\n❌ Password 'admin123' SAI!")
                    print("   → Cần cập nhật lại password")
                    
                    # Fix password
                    print("\n🔧 Đang cập nhật password...")
                    new_hashed = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    
                    update_sql = text("UPDATE [USER] SET PasswordHash = :password WHERE Username = :username")
                    conn.execute(update_sql, {
                        "password": new_hashed,
                        "username": "admin"
                    })
                    
                    print("✅ Đã cập nhật password thành công!")
                    print("   Username: admin")
                    print("   Password: admin123")
                    
            except ValueError as e:
                print(f"\n❌ Password hash KHÔNG HỢP LỆ!")
                print(f"   Lỗi: {e}")
                print("   → Hash không phải bcrypt format")
                
                # Fix password
                print("\n🔧 Đang tạo lại password với bcrypt...")
                new_hashed = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                update_sql = text("UPDATE [USER] SET PasswordHash = :password WHERE Username = :username")
                conn.execute(update_sql, {
                    "password": new_hashed,
                    "username": "admin"
                })
                
                print("✅ Đã tạo lại password thành công!")
                print("   Username: admin")
                print("   Password: admin123")
                
            except Exception as e:
                print(f"\n❌ Lỗi không xác định: {e}")

if __name__ == "__main__":
    try:
        fix_admin_password()
        print("\n" + "="*50)
        print("🎯 Bây giờ hãy thử login lại với:")
        print("   Username: admin")
        print("   Password: admin123")
        print("="*50)
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
