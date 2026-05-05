"""
Tạo lại user admin với password đúng
"""
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

def create_admin_user():
    """Tạo user admin với password admin123"""
    
    # Generate password hash
    password = "admin123"
    password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    print(f"Password: {password}")
    print(f"Hash: {password_hash}")
    
    # Connect to database
    engine = create_engine(SQL_SERVER_PERMISSION_CONN)
    
    with engine.connect() as conn:
        # 1. Kiểm tra user admin có tồn tại không
        result = conn.execute(text("SELECT UserID, Username FROM [USER] WHERE Username = 'admin'"))
        admin_user = result.fetchone()
        
        if admin_user:
            print(f"\n✅ User admin đã tồn tại (UserID: {admin_user[0]})")
            
            # Update password
            conn.execute(text("""
                UPDATE [USER] 
                SET PasswordHash = :password_hash,
                    Email = 'admin@company.com',
                    Status = 'ACTIVE'
                WHERE Username = 'admin'
            """), {"password_hash": password_hash})
            conn.commit()
            
            print("✅ Đã cập nhật password mới!")
            admin_id = admin_user[0]
            
        else:
            print("\n❌ User admin không tồn tại, tạo mới...")
            
            # Create new admin user
            result = conn.execute(text("""
                INSERT INTO [USER] (Username, PasswordHash, Email, Status, CreatedAt)
                OUTPUT INSERTED.UserID
                VALUES ('admin', :password_hash, 'admin@company.com', 'ACTIVE', GETDATE())
            """), {"password_hash": password_hash})
            
            admin_id = result.fetchone()[0]
            conn.commit()
            
            print(f"✅ Đã tạo user admin mới (UserID: {admin_id})")
        
        # 2. Gán role SUPER_ADMIN
        result = conn.execute(text("SELECT RoleID FROM ROLE WHERE RoleName = 'SUPER_ADMIN'"))
        super_admin_role = result.fetchone()
        
        if super_admin_role:
            role_id = super_admin_role[0]
            
            # Xóa role cũ
            conn.execute(text("DELETE FROM USER_ROLE WHERE UserID = :user_id"), {"user_id": admin_id})
            
            # Gán role mới
            conn.execute(text("""
                INSERT INTO USER_ROLE (UserID, RoleID, AssignedAt)
                VALUES (:user_id, :role_id, GETDATE())
            """), {"user_id": admin_id, "role_id": role_id})
            conn.commit()
            
            print(f"✅ Đã gán role SUPER_ADMIN cho admin!")
        else:
            print("❌ Role SUPER_ADMIN không tồn tại!")
        
        # 3. Verify
        result = conn.execute(text("""
            SELECT 
                u.UserID,
                u.Username,
                u.Email,
                u.Status,
                r.RoleName
            FROM [USER] u
            LEFT JOIN USER_ROLE ur ON u.UserID = ur.UserID
            LEFT JOIN ROLE r ON ur.RoleID = r.RoleID
            WHERE u.Username = 'admin'
        """))
        
        user_info = result.fetchone()
        if user_info:
            print(f"\n📊 Thông tin user admin:")
            print(f"  - UserID: {user_info[0]}")
            print(f"  - Username: {user_info[1]}")
            print(f"  - Email: {user_info[2]}")
            print(f"  - Status: {user_info[3]}")
            print(f"  - Role: {user_info[4]}")
        
        print("\n🎉 Hoàn thành! Bây giờ có thể đăng nhập với:")
        print("   Username: admin")
        print("   Password: admin123")

if __name__ == "__main__":
    try:
        create_admin_user()
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
