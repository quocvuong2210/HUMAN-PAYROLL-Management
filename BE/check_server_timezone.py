"""
Kiểm tra timezone của server và database
"""
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN
import datetime

def check_timezone():
    """Kiểm tra timezone"""
    print("="*70)
    print("🌍 KIỂM TRA TIMEZONE")
    print("="*70)
    
    # 1. Python timezone
    print("\n1️⃣ Python Server Timezone:")
    now_local = datetime.datetime.now()
    now_utc = datetime.datetime.utcnow()
    
    print(f"   Local time: {now_local}")
    print(f"   UTC time: {now_utc}")
    print(f"   Offset: {now_local - now_utc}")
    
    # 2. Database timezone
    print("\n2️⃣ SQL Server Timezone:")
    engine = create_engine(SQL_SERVER_PERMISSION_CONN)
    
    with engine.connect() as conn:
        # Get current database time
        sql = text("SELECT GETDATE() AS ServerTime, GETUTCDATE() AS UTCTime")
        result = conn.execute(sql).fetchone()
        
        server_time = result[0]
        utc_time = result[1]
        
        print(f"   Server time (GETDATE): {server_time}")
        print(f"   UTC time (GETUTCDATE): {utc_time}")
        print(f"   Offset: {server_time - utc_time}")
        
        # Check timezone offset
        sql2 = text("SELECT SYSDATETIMEOFFSET() AS TimeWithOffset")
        result2 = conn.execute(sql2).fetchone()
        print(f"   Time with offset: {result2[0]}")
    
    # 3. Check latest log
    print("\n3️⃣ Latest Access Log:")
    with engine.connect() as conn:
        sql = text("""
            SELECT TOP 1
                LogID,
                UserID,
                Action,
                AccessTime
            FROM [ACCESS_LOG]
            ORDER BY AccessTime DESC
        """)
        
        result = conn.execute(sql).fetchone()
        
        if result:
            print(f"   LogID: {result[0]}")
            print(f"   UserID: {result[1]}")
            print(f"   Action: {result[2]}")
            print(f"   AccessTime (from DB): {result[3]}")
            print(f"   Type: {type(result[3])}")
    
    # 4. Recommendation
    print("\n" + "="*70)
    print("💡 KHUYẾN NGHỊ:")
    print("="*70)
    
    if (now_local - now_utc).total_seconds() < 3600:  # Less than 1 hour offset
        print("\n⚠️  Server đang dùng UTC hoặc gần UTC")
        print("   → Backend đang lưu thời gian UTC")
        print("   → Frontend convert sang giờ địa phương (+7 giờ)")
        print("   → Kết quả: Thời gian có thể vượt sang ngày hôm sau")
        print("\n🔧 GIẢI PHÁP:")
        print("   1. Backend lưu thời gian theo timezone Việt Nam")
        print("   2. Hoặc Frontend hiển thị UTC time")
        print("   3. Hoặc thêm timezone info vào database")
    else:
        print("\n✅ Server đang dùng timezone địa phương")
        print("   → Thời gian nên hiển thị đúng")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        check_timezone()
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
