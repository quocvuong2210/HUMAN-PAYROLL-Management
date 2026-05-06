"""
Test password trực tiếp - Không cần server
"""
import bcrypt
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

def test_password_direct():
    """Test password trực tiếp với database"""
    print("="*70)
    print("🔐 TEST PASSWORD TRỰC TIẾP")
    print("="*70)
    
    username = "admin"
    password = "admin123"
    
    try:
        engine = create_engine(SQL_SERVER_PERMISSION_CONN)
        
        print(f"\n1️⃣ Kết nối database...")
        print(f"   ✅ Connected")
        
        print(f"\n2️⃣ Tìm user '{username}'...")
        with engine.connect() as conn:
            sql = text("SELECT UserID, Username, PasswordHash, Status, EmailVerified FROM [USER] WHERE Username = :username")
            result = conn.execute(sql, {"username": username}).fetchone()
            
            if not result:
                print(f"   ❌ User '{username}' KHÔNG TỒN TẠI!")
                print(f"\n🔧 Tạo user mới...")
                
                with conn.begin():
                    # Tạo hash mới
                    new_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    
                    insert_sql = text("""
                        INSERT INTO [USER] (Username, PasswordHash, Email, Status, EmailVerified)
                        VALUES (:username, :password, :email, :status, :verified)
                    """)
                    
                    conn.execute(insert_sql, {
                        "username": username,
                        "password": new_hash,
                        "email": "admin@company.com",
                        "status": "ACTIVE",
                        "verified": 1
                    })
                    
                    print(f"   ✅ Đã tạo user '{username}'")
                    print(f"   Password: {password}")
                    print(f"   Hash: {new_hash[:50]}...")
                    
                print("\n" + "="*70)
                print("🎉 USER ĐÃ ĐƯỢC TẠO!")
                print("="*70)
                print(f"\n📝 Thông tin đăng nhập:")
                print(f"   Username: {username}")
                print(f"   Password: {password}")
                print("\n🔄 Hãy thử login lại!")
                return
            
            user_id = result[0]
            db_username = result[1]
            password_hash = result[2]
            status = result[3]
            email_verified = result[4]
            
            print(f"   ✅ User tồn tại")
            print(f"      UserID: {user_id}")
            print(f"      Username: {db_username}")
            print(f"      Status: {status}")
            print(f"      EmailVerified: {email_verified}")
            print(f"      Hash length: {len(password_hash)} chars")
            print(f"      Hash: {password_hash[:60]}...")
            
            # Kiểm tra Status
            print(f"\n3️⃣ Kiểm tra Status...")
            if status != 'ACTIVE':
                print(f"   ❌ Status = '{status}' (cần ACTIVE)")
                print(f"   🔧 Đang fix...")
                
                with conn.begin():
                    update_sql = text("UPDATE [USER] SET Status = 'ACTIVE' WHERE Username = :username")
                    conn.execute(update_sql, {"username": username})
                    print(f"   ✅ Đã cập nhật Status = 'ACTIVE'")
            else:
                print(f"   ✅ Status = 'ACTIVE'")
            
            # Kiểm tra hash format
            print(f"\n4️⃣ Kiểm tra hash format...")
            if password_hash.startswith('$2b$') or password_hash.startswith('$2a$') or password_hash.startswith('$2y$'):
                print(f"   ✅ Hash format: bcrypt")
            else:
                print(f"   ❌ Hash format KHÔNG PHẢI bcrypt!")
                print(f"      Hash bắt đầu: {password_hash[:20]}")
                print(f"   🔧 Đang tạo lại hash...")
                
                with conn.begin():
                    new_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    update_sql = text("UPDATE [USER] SET PasswordHash = :password WHERE Username = :username")
                    conn.execute(update_sql, {"password": new_hash, "username": username})
                    
                    print(f"   ✅ Đã tạo lại hash bcrypt")
                    password_hash = new_hash
            
            # Test password
            print(f"\n5️⃣ Test password '{password}'...")
            print(f"   Password bytes: {password.encode('utf-8')}")
            print(f"   Hash bytes length: {len(password_hash.encode('utf-8'))}")
            
            try:
                is_valid = bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
                
                if is_valid:
                    print(f"   ✅ PASSWORD ĐÚNG!")
                    print("\n" + "="*70)
                    print("🎉 LOGIN SẼ HOẠT ĐỘNG!")
                    print("="*70)
                    print(f"\n📝 Thông tin đăng nhập:")
                    print(f"   Username: {username}")
                    print(f"   Password: {password}")
                    print("\n✅ Mọi thứ đã OK!")
                    print("🔄 Hãy RESTART backend và thử login lại!")
                    
                else:
                    print(f"   ❌ PASSWORD SAI!")
                    print(f"\n🔧 Đang fix password...")
                    
                    # Tạo hash mới
                    new_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    print(f"   New hash: {new_hash[:50]}...")
                    
                    # Verify hash mới trước khi update
                    is_valid_new = bcrypt.checkpw(password.encode('utf-8'), new_hash.encode('utf-8'))
                    print(f"   Verify new hash: {'✅ ĐÚNG' if is_valid_new else '❌ SAI'}")
                    
                    # Update database
                    update_sql = text("UPDATE [USER] SET PasswordHash = :password WHERE Username = :username")
                    conn.execute(update_sql, {"password": new_hash, "username": username})
                    conn.commit()
                    
                    print(f"   ✅ Đã cập nhật password!")
                        
                    print("\n" + "="*70)
                    print("🎉 PASSWORD ĐÃ ĐƯỢC FIX!")
                    print("="*70)
                    print(f"\n📝 Thông tin đăng nhập:")
                    print(f"   Username: {username}")
                    print(f"   Password: {password}")
                    print("\n🔄 Hãy RESTART backend và thử login lại!")
                    
            except ValueError as e:
                print(f"   ❌ ValueError: {e}")
                print(f"   → Hash không đúng format bcrypt")
                print(f"\n🔧 Đang tạo lại hash...")
                
                new_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                update_sql = text("UPDATE [USER] SET PasswordHash = :password WHERE Username = :username")
                conn.execute(update_sql, {"password": new_hash, "username": username})
                conn.commit()
                
                print(f"   ✅ Đã tạo lại hash!")
                print(f"   New hash: {new_hash[:50]}...")
                    
                print("\n" + "="*70)
                print("🎉 PASSWORD ĐÃ ĐƯỢC FIX!")
                print("="*70)
                print(f"\n📝 Thông tin đăng nhập:")
                print(f"   Username: {username}")
                print(f"   Password: {password}")
                print("\n🔄 Hãy RESTART backend và thử login lại!")
                
            except Exception as e:
                print(f"   ❌ Exception: {e}")
                import traceback
                traceback.print_exc()
                
    except Exception as e:
        print(f"\n❌ Lỗi kết nối database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_password_direct()
    print("\n" + "="*70)
