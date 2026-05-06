"""
Kiểm tra access logs trong database
"""
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

def check_access_logs():
    """Kiểm tra access logs"""
    engine = create_engine(SQL_SERVER_PERMISSION_CONN)
    
    print("="*70)
    print("📋 KIỂM TRA ACCESS LOGS")
    print("="*70)
    
    with engine.connect() as conn:
        # 1. Kiểm tra bảng ACCESS_LOG có tồn tại không
        print("\n1️⃣ Kiểm tra bảng ACCESS_LOG...")
        try:
            check_table = text("""
                SELECT COUNT(*) as Count
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_NAME = 'ACCESS_LOG'
            """)
            result = conn.execute(check_table).fetchone()
            
            if result[0] == 0:
                print("   ❌ Bảng ACCESS_LOG KHÔNG TỒN TẠI!")
                print("   → Cần chạy lại database setup script")
                return
            else:
                print("   ✅ Bảng ACCESS_LOG tồn tại")
        except Exception as e:
            print(f"   ❌ Lỗi: {e}")
            return
        
        # 2. Đếm số lượng logs
        print("\n2️⃣ Đếm số lượng logs...")
        count_sql = text("SELECT COUNT(*) as Count FROM [ACCESS_LOG]")
        count_result = conn.execute(count_sql).fetchone()
        total_logs = count_result[0]
        
        print(f"   📊 Tổng số logs: {total_logs}")
        
        if total_logs == 0:
            print("   ⚠️  Chưa có log nào!")
            print("   → Thử đăng nhập để tạo log")
            return
        
        # 3. Lấy 10 logs mới nhất
        print("\n3️⃣ 10 logs mới nhất:")
        print("-"*70)
        
        logs_sql = text("""
            SELECT TOP 10
                L.LogID,
                L.UserID,
                U.Username,
                L.Action,
                L.IPAddress,
                L.AccessTime
            FROM [ACCESS_LOG] L
            LEFT JOIN [USER] U ON L.UserID = U.UserID
            ORDER BY L.AccessTime DESC
        """)
        
        logs = conn.execute(logs_sql).fetchall()
        
        for log in logs:
            log_id = log[0]
            user_id = log[1]
            username = log[2] if log[2] else "(deleted user)"
            action = log[3]
            ip = log[4]
            access_time = log[5]
            
            action_icon = "✅" if "SUCCESS" in action else "❌"
            
            print(f"\n{action_icon} LogID: {log_id}")
            print(f"   User: {username} (ID: {user_id})")
            print(f"   Action: {action}")
            print(f"   IP: {ip}")
            print(f"   Time: {access_time}")
        
        # 4. Thống kê theo action
        print("\n" + "="*70)
        print("4️⃣ Thống kê theo Action:")
        print("-"*70)
        
        stats_sql = text("""
            SELECT Action, COUNT(*) as Count
            FROM [ACCESS_LOG]
            GROUP BY Action
            ORDER BY Count DESC
        """)
        
        stats = conn.execute(stats_sql).fetchall()
        
        for stat in stats:
            action = stat[0]
            count = stat[1]
            print(f"   {action}: {count} lần")
        
        # 5. Logs của user admin
        print("\n" + "="*70)
        print("5️⃣ Logs của user 'admin':")
        print("-"*70)
        
        admin_logs_sql = text("""
            SELECT TOP 5
                L.Action,
                L.IPAddress,
                L.AccessTime
            FROM [ACCESS_LOG] L
            INNER JOIN [USER] U ON L.UserID = U.UserID
            WHERE U.Username = 'admin'
            ORDER BY L.AccessTime DESC
        """)
        
        admin_logs = conn.execute(admin_logs_sql).fetchall()
        
        if not admin_logs:
            print("   ⚠️  Chưa có log nào của user 'admin'")
        else:
            for log in admin_logs:
                action = log[0]
                ip = log[1]
                time = log[2]
                print(f"   • {action} - {ip} - {time}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        check_access_logs()
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
