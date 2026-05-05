"""
Script kiểm tra passwords trong database
Kiểm tra xem passwords có đúng format hash không
"""
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

def check_passwords():
    """Kiểm tra tất cả passwords trong database"""
    engine = create_engine(SQL_SERVER_PERMISSION_CONN)
    
    print("🔍 Đang kiểm tra passwords trong database...")
    print("=" * 80)
    
    with engine.connect() as conn:
        # Lấy tất cả users
        sql = text("""
            SELECT UserID, Username, [Password], [Status]
            FROM [USER]
            ORDER BY UserID
        """)
        
        result = conn.execute(sql)
        users = result.fetchall()
        
        if not users:
            print("⚠️  Không có user nào trong database")
            return
        
        print(f"Tìm thấy {len(users)} users:\n")
        
        valid_count = 0
        invalid_count = 0
        
        for user in users:
            user_id = user[0]
            username = user[1]
            password_hash = user[2]
            status = user[3]
            
            # Kiểm tra format hash
            # pbkdf2:sha256 hash format: pbkdf2:sha256:ITERATIONS$SALT$HASH
            is_valid = password_hash and password_hash.startswith('pbkdf2:sha256:')
            
            if is_valid:
                valid_count += 1
                print(f"✅ UserID {user_id}: {username:20} | Status: {status:10} | Hash: VALID")
                print(f"   {password_hash[:60]}...")
            else:
                invalid_count += 1
                print(f"❌ UserID {user_id}: {username:20} | Status: {status:10} | Hash: INVALID")
                print(f"   {password_hash[:60] if password_hash else 'NULL'}...")
            
            print()
    
    print("=" * 80)
    print(f"📊 Tổng kết:")
    print(f"   ✅ Valid passwords: {valid_count}")
    print(f"   ❌ Invalid passwords: {invalid_count}")
    
    if invalid_count > 0:
        print(f"\n⚠️  CÓ {invalid_count} PASSWORDS KHÔNG HỢP LỆ!")
        print("   Chạy: python reset_passwords.py để sửa")
    else:
        print("\n✅ TẤT CẢ PASSWORDS ĐỀU HỢP LỆ!")

if __name__ == "__main__":
    try:
        check_passwords()
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()
