"""
Kiểm tra tất cả users trong database
"""
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

def check_all_users():
    """Kiểm tra tất cả users"""
    engine = create_engine(SQL_SERVER_PERMISSION_CONN)
    
    print("="*70)
    print("👥 DANH SÁCH TẤT CẢ USERS")
    print("="*70)
    
    with engine.connect() as conn:
        sql = text("""
            SELECT UserID, Username, Email, Status, EmailVerified, CreatedAt
            FROM [USER]
            ORDER BY UserID
        """)
        
        results = conn.execute(sql).fetchall()
        
        if not results:
            print("\n❌ Không có user nào trong database!")
            return
        
        print(f"\n📊 Tổng số users: {len(results)}")
        print("\n" + "-"*70)
        
        for row in results:
            user_id = row[0]
            username = row[1]
            email = row[2]
            status = row[3]
            email_verified = row[4]
            created_at = row[5]
            
            status_icon = "✅" if status == "ACTIVE" else "❌"
            
            print(f"\n{status_icon} UserID: {user_id}")
            print(f"   Username: {username}")
            print(f"   Email: {email}")
            print(f"   Status: {status}")
            print(f"   EmailVerified: {email_verified}")
            print(f"   CreatedAt: {created_at}")
            
            # Lấy roles
            role_sql = text("""
                SELECT R.RoleName
                FROM [USER_ROLE] UR
                INNER JOIN [ROLE] R ON UR.RoleID = R.RoleID
                WHERE UR.UserID = :user_id
            """)
            
            roles = conn.execute(role_sql, {"user_id": user_id}).fetchall()
            if roles:
                role_names = [r[0] for r in roles]
                print(f"   Roles: {', '.join(role_names)}")
            else:
                print(f"   Roles: (none)")
        
        print("\n" + "="*70)
        print("\n🔧 HÀNH ĐỘNG CẦN LÀM:")
        print("="*70)
        
        # Tìm user 'a'
        user_a = [r for r in results if r[1] == 'a']
        if user_a:
            print(f"\n⚠️  Tìm thấy user 'a' (UserID: {user_a[0][0]})")
            print(f"   Status: {user_a[0][3]}")
            print("\n   Tùy chọn:")
            print(f"   1. Đổi username 'a' → 'admin'")
            print(f"   2. Xóa user 'a'")
            print(f"   3. Kích hoạt user 'a' (nếu bị khóa)")
        
        # Tìm user 'admin'
        user_admin = [r for r in results if r[1] == 'admin']
        if not user_admin:
            print(f"\n❌ KHÔNG tìm thấy user 'admin'!")
            print(f"   → Cần tạo lại user admin")
        elif user_admin[0][3] != 'ACTIVE':
            print(f"\n⚠️  User 'admin' bị khóa (Status: {user_admin[0][3]})")
            print(f"   → Cần kích hoạt lại")

if __name__ == "__main__":
    try:
        check_all_users()
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
