"""
Debug script - Kiểm tra chi tiết quá trình login
"""
import bcrypt
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

def debug_login():
    """Debug chi tiết quá trình login"""
    engine = create_engine(SQL_SERVER_PERMISSION_CONN)
    
    print("="*60)
    print("🔍 DEBUG LOGIN PROCESS")
    print("="*60)
    
    with engine.connect() as conn:
        # 1. Kiểm tra user admin
        print("\n1️⃣ Kiểm tra user admin trong database...")
        check_sql = text("SELECT UserID, Username, PasswordHash, Email, Status, EmailVerified FROM [USER] WHERE Username = :username")
        result = conn.execute(check_sql, {"username": "admin"}).fetchone()
        
        if not result:
            print("   ❌ User 'admin' KHÔNG tồn tại!")
            print("\n   🔧 Hãy chạy: python BE/fix_admin_password.py")
            return
        
        print("   ✅ User 'admin' tồn tại")
        user_id = result[0]
        username = result[1]
        password_hash = result[2]
        email = result[3]
        status = result[4]
        email_verified = result[5]
        
        print(f"      UserID: {user_id}")
        print(f"      Username: {username}")
        print(f"      Email: {email}")
        print(f"      Status: {status}")
        print(f"      EmailVerified: {email_verified}")
        print(f"      PasswordHash length: {len(password_hash)} chars")
        print(f"      PasswordHash prefix: {password_hash[:20]}...")
        
        # 2. Kiểm tra Status
        print("\n2️⃣ Kiểm tra Status...")
        if status != 'ACTIVE':
            print(f"   ❌ Status = '{status}' (phải là 'ACTIVE')")
            print("   🔧 Đang fix...")
            update_sql = text("UPDATE [USER] SET Status = 'ACTIVE' WHERE Username = :username")
            conn.execute(update_sql, {"username": "admin"})
            conn.commit()
            print("   ✅ Đã cập nhật Status = 'ACTIVE'")
        else:
            print("   ✅ Status = 'ACTIVE'")
        
        # 3. Kiểm tra password hash format
        print("\n3️⃣ Kiểm tra password hash format...")
        if password_hash.startswith('$2b$') or password_hash.startswith('$2a$') or password_hash.startswith('$2y$'):
            print(f"   ✅ Hash format: bcrypt ({password_hash[:4]}...)")
        else:
            print(f"   ❌ Hash format KHÔNG PHẢI bcrypt!")
            print(f"      Hash bắt đầu bằng: {password_hash[:10]}")
            print("   🔧 Cần tạo lại password với bcrypt")
            
            new_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            update_sql = text("UPDATE [USER] SET PasswordHash = :password WHERE Username = :username")
            conn.execute(update_sql, {"password": new_hash, "username": "admin"})
            conn.commit()
            print("   ✅ Đã tạo lại password hash với bcrypt")
            password_hash = new_hash
        
        # 4. Test password verification
        print("\n4️⃣ Test password verification...")
        test_password = "admin123"
        
        try:
            print(f"   Testing password: '{test_password}'")
            print(f"   Against hash: {password_hash[:30]}...")
            
            # Encode password
            password_bytes = test_password.encode('utf-8')
            hash_bytes = password_hash.encode('utf-8')
            
            print(f"   Password bytes length: {len(password_bytes)}")
            print(f"   Hash bytes length: {len(hash_bytes)}")
            
            # Check password
            is_valid = bcrypt.checkpw(password_bytes, hash_bytes)
            
            if is_valid:
                print("   ✅ Password ĐÚNG!")
                print("\n" + "="*60)
                print("🎉 LOGIN SẼ HOẠT ĐỘNG!")
                print("="*60)
                print("\n📝 Thông tin đăng nhập:")
                print("   Username: admin")
                print("   Password: admin123")
                print("\n🔄 Hãy thử login lại từ frontend!")
            else:
                print("   ❌ Password SAI!")
                print("\n🔧 Đang tạo lại password...")
                
                new_hash = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                update_sql = text("UPDATE [USER] SET PasswordHash = :password WHERE Username = :username")
                conn.execute(update_sql, {"password": new_hash, "username": "admin"})
                conn.commit()
                
                print("   ✅ Đã tạo lại password!")
                print("\n" + "="*60)
                print("🎉 PASSWORD ĐÃ ĐƯỢC FIX!")
                print("="*60)
                print("\n📝 Thông tin đăng nhập:")
                print("   Username: admin")
                print("   Password: admin123")
                print("\n🔄 Hãy thử login lại từ frontend!")
                
        except ValueError as e:
            print(f"   ❌ ValueError: {e}")
            print("   → Hash không đúng format bcrypt")
            
            print("\n🔧 Đang tạo lại password với bcrypt...")
            new_hash = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            update_sql = text("UPDATE [USER] SET PasswordHash = :password WHERE Username = :username")
            conn.execute(update_sql, {"password": new_hash, "username": "admin"})
            conn.commit()
            
            print("   ✅ Đã tạo lại password!")
            print("\n" + "="*60)
            print("🎉 PASSWORD ĐÃ ĐƯỢC FIX!")
            print("="*60)
            print("\n📝 Thông tin đăng nhập:")
            print("   Username: admin")
            print("   Password: admin123")
            print("\n🔄 Hãy thử login lại từ frontend!")
            
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    try:
        debug_login()
    except Exception as e:
        print(f"\n❌ Lỗi kết nối database: {e}")
        import traceback
        traceback.print_exc()
