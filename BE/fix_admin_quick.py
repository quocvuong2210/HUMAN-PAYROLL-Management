"""
Sửa nhanh user admin
"""
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

# Generate password hash
password = "admin123"
password_hash = generate_password_hash(password, method='pbkdf2:sha256')

print(f"🔑 Password: {password}")
print(f"🔐 Hash: {password_hash[:50]}...")

# Connect to database
engine = create_engine(SQL_SERVER_PERMISSION_CONN)

with engine.connect() as conn:
    # Fix user với UserID = 1
    conn.execute(text("""
        UPDATE [USER] 
        SET Username = 'admin',
            Password = :password_hash,
            Email = 'admin@company.com',
            Status = 'ACTIVE',
            PhoneNumber = '0901234567',
            DateOfBirth = '1990-01-15',
            Gender = 'Nam'
        WHERE UserID = 1
    """), {"password_hash": password_hash})
    conn.commit()
    
    print("\n✅ Đã sửa user admin (UserID=1)!")
    
    # Verify
    result = conn.execute(text("""
        SELECT 
            u.UserID,
            u.Username,
            u.Email,
            u.PhoneNumber,
            u.DateOfBirth,
            u.Gender,
            u.Status,
            r.RoleName
        FROM [USER] u
        LEFT JOIN USER_ROLE ur ON u.UserID = ur.UserID
        LEFT JOIN ROLE r ON ur.RoleID = r.RoleID
        WHERE u.UserID = 1
    """))
    
    user_info = result.fetchone()
    if user_info:
        print(f"\n📊 Thông tin user admin:")
        print(f"  - UserID: {user_info[0]}")
        print(f"  - Username: {user_info[1]}")
        print(f"  - Email: {user_info[2]}")
        print(f"  - Phone: {user_info[3]}")
        print(f"  - DOB: {user_info[4]}")
        print(f"  - Gender: {user_info[5]}")
        print(f"  - Status: {user_info[6]}")
        print(f"  - Role: {user_info[7]}")
    
    print("\n🎉 Hoàn thành! Bây giờ có thể đăng nhập với:")
    print("   Username: admin")
    print("   Password: admin123")

print("\n✅ Xong! Hãy thử đăng nhập lại!")
