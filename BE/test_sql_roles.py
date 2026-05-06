"""
Test SQL query for roles
"""
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

def test_sql_roles():
    """Test SQL query"""
    engine = create_engine(SQL_SERVER_PERMISSION_CONN)
    
    print("="*70)
    print("🔍 TEST SQL ROLES QUERY")
    print("="*70)
    
    with engine.connect() as conn:
        # Test access logs query
        print("\n1️⃣ Test Access Logs Query...")
        sql = text("""
            SELECT 
                UAL.LogID,
                UAL.UserID,
                UAL.Action,
                U.Username,
                U.Email,
                -- Get user roles
                STUFF((
                    SELECT ',' + R.RoleName
                    FROM [USER_ROLE] UR
                    INNER JOIN [ROLE] R ON UR.RoleID = R.RoleID
                    WHERE UR.UserID = U.UserID
                    FOR XML PATH('')
                ), 1, 1, '') AS UserRoles
            FROM [ACCESS_LOG] UAL
            INNER JOIN [USER] U ON UAL.UserID = U.UserID
            ORDER BY UAL.AccessTime DESC
        """)
        
        results = conn.execute(sql).fetchall()
        
        print(f"   Số lượng logs: {len(results)}")
        
        if results:
            print(f"\n   📋 3 logs đầu tiên:")
            for i, row in enumerate(results[:3], 1):
                print(f"\n   {i}. LogID: {row[0]}")
                print(f"      UserID: {row[1]}")
                print(f"      Action: {row[2]}")
                print(f"      Username: {row[3]}")
                print(f"      Email: {row[4]}")
                print(f"      UserRoles: {row[5]}")
                print(f"      UserRoles type: {type(row[5])}")
                print(f"      UserRoles is None: {row[5] is None}")
        
        # Test users query
        print("\n" + "="*70)
        print("2️⃣ Test Users Query...")
        sql2 = text("""
            SELECT 
                U.UserID,
                U.Username,
                -- Get roles
                STUFF((
                    SELECT ',' + R.RoleName
                    FROM [USER_ROLE] UR
                    INNER JOIN [ROLE] R ON UR.RoleID = R.RoleID
                    WHERE UR.UserID = U.UserID
                    FOR XML PATH('')
                ), 1, 1, '') AS Roles
            FROM [USER] U
            ORDER BY U.UserID
        """)
        
        users = conn.execute(sql2).fetchall()
        
        print(f"   Số lượng users: {len(users)}")
        
        if users:
            print(f"\n   👥 Danh sách users:")
            for user in users:
                print(f"\n   • UserID: {user[0]}")
                print(f"     Username: {user[1]}")
                print(f"     Roles: {user[2]}")
                print(f"     Roles type: {type(user[2])}")
                print(f"     Roles is None: {user[2] is None}")
        
        # Check USER_ROLE table
        print("\n" + "="*70)
        print("3️⃣ Check USER_ROLE table...")
        sql3 = text("""
            SELECT 
                UR.UserID,
                U.Username,
                UR.RoleID,
                R.RoleName
            FROM [USER_ROLE] UR
            INNER JOIN [USER] U ON UR.UserID = U.UserID
            INNER JOIN [ROLE] R ON UR.RoleID = R.RoleID
            ORDER BY UR.UserID
        """)
        
        user_roles = conn.execute(sql3).fetchall()
        
        print(f"   Số lượng user-role mappings: {len(user_roles)}")
        
        if user_roles:
            print(f"\n   🔗 User-Role Mappings:")
            for ur in user_roles:
                print(f"   • {ur[1]} (UserID: {ur[0]}) → {ur[3]} (RoleID: {ur[2]})")
        else:
            print(f"   ⚠️  KHÔNG CÓ user-role mapping nào!")
            print(f"   → Đây là nguyên nhân roles không hiển thị!")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        test_sql_roles()
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
