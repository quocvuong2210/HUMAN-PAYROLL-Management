"""
Script để reset TẤT CẢ passwords trong database
Chạy script này để reset tất cả users với hash method đúng
"""
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash
from config import SQL_SERVER_PERMISSION_CONN

def reset_all_passwords():
    """Reset passwords cho TẤT CẢ users trong database"""
    engine = create_engine(SQL_SERVER_PERMISSION_CONN)
    
    # Default password cho tất cả users
    default_password = "admin123"
    
    print("🔄 Đang reset TẤT CẢ passwords với method='pbkdf2:sha256'...")
    print("=" * 80)
    
    with engine.connect() as conn:
        with conn.begin():
            # Lấy tất cả users
            sql_get = text("""
                SELECT UserID, Username, [Status]
                FROM [USER]
                ORDER BY UserID
            """)
            
            result = conn.execute(sql_get)
            users = result.fetchall()
            
            if not users:
                print("⚠️  Không có user nào trong database")
                return
            
            print(f"Tìm thấy {len(users)} users. Đang reset passwords...\n")
            
            success_count = 0
            
            for user in users:
                user_id = user[0]
                username = user[1]
                status = user[2]
                
                # Hash password với method='pbkdf2:sha256'
                hashed_password = generate_password_hash(default_password, method='pbkdf2:sha256')
                
                # Update password và set status = ACTIVE
                sql_update = text("""
                    UPDATE [USER]
                    SET [Password] = :password, [Status] = 'ACTIVE'
                    WHERE UserID = :user_id
                """)
                
                try:
                    conn.execute(sql_update, {
                        "password": hashed_password,
                        "user_id": user_id
                    })
                    
                    success_count += 1
                    print(f"✅ UserID {user_id:3}: {username:20} | Old Status: {status:10} → New: ACTIVE")
                    print(f"   Password: {default_password}")
                    print(f"   Hash: {hashed_password[:60]}...")
                    print()
                    
                except Exception as e:
                    print(f"❌ UserID {user_id:3}: {username:20} | Error: {str(e)}")
                    print()
    
    print("=" * 80)
    print(f"✅ Hoàn thành! Reset {success_count}/{len(users)} users")
    print(f"\n⚠️  TẤT CẢ USERS HIỆN CÓ PASSWORD: {default_password}")
    print("\nSample users:")
    print("  - admin / admin123 → SUPER_ADMIN")
    print("  - hr_manager / admin123 → HR_MANAGER")
    print("  - accountant / admin123 → PAYROLL_ACCOUNTANT")
    print("  - employee / admin123 → EMPLOYEE")
    print("  - testuser_updated / admin123")
    print("  - newuser / admin123")
    print("  - sang / admin123")
    print("  - testuser / admin123")
    print("\n⚠️  LƯU Ý: Tất cả passwords đã được hash với method='pbkdf2:sha256'")
    print("⚠️  LƯU Ý: Tất cả users đã được set Status = ACTIVE")

if __name__ == "__main__":
    try:
        # Confirm before running
        print("⚠️  CẢNH BÁO: Script này sẽ reset TẤT CẢ passwords trong database!")
        print(f"   Tất cả users sẽ có password: admin123")
        print(f"   Tất cả users sẽ có Status: ACTIVE")
        print()
        
        confirm = input("Bạn có chắc chắn muốn tiếp tục? (yes/no): ")
        
        if confirm.lower() in ['yes', 'y']:
            print()
            reset_all_passwords()
        else:
            print("\n❌ Đã hủy!")
            
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()
