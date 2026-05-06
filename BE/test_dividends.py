"""
Test Dividends - Kiểm tra bảng và tạo dữ liệu mẫu
"""
from sqlalchemy import create_engine, text
from config import SQL_SERVER_CONN

def test_dividends():
    print("=" * 60)
    print("🧪 TEST DIVIDENDS")
    print("=" * 60)
    
    engine = create_engine(SQL_SERVER_CONN)
    
    # 1. Kiểm tra bảng Employees
    print("\n1️⃣ Kiểm tra bảng Employees...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT TOP 5 EmployeeID, FullName FROM [Employees]"))
            employees = result.fetchall()
            
            if employees:
                print(f"   ✅ Bảng Employees tồn tại ({len(employees)} nhân viên)")
                for emp in employees:
                    print(f"      - ID: {emp[0]}, Tên: {emp[1]}")
            else:
                print("   ⚠️ Bảng Employees trống")
                print("   💡 Cần thêm nhân viên trước!")
                return
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")
        print("   💡 Bảng Employees chưa tồn tại!")
        return
    
    # 2. Kiểm tra bảng Dividends
    print("\n2️⃣ Kiểm tra bảng Dividends...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) as Count FROM [Dividends]"))
            count = result.fetchone()[0]
            print(f"   ✅ Bảng Dividends tồn tại ({count} thưởng)")
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")
        print("   💡 Cần chạy script: BE/database/ADD_DIVIDENDS_TABLE.sql")
        return
    
    # 3. Tạo dữ liệu mẫu
    print("\n3️⃣ Tạo dữ liệu mẫu...")
    try:
        with engine.connect() as conn:
            with conn.begin():
                # Lấy EmployeeID đầu tiên
                result = conn.execute(text("SELECT TOP 1 EmployeeID FROM [Employees]"))
                employee_id = result.fetchone()[0]
                
                # Tạo 3 thưởng mẫu (chỉ 3 cột)
                samples = [
                    {
                        "emp_id": employee_id,
                        "amount": 5000000,
                        "date": "2026-01-15"
                    },
                    {
                        "emp_id": employee_id,
                        "amount": 3000000,
                        "date": "2026-03-01"
                    },
                    {
                        "emp_id": employee_id,
                        "amount": 2000000,
                        "date": "2026-05-06"
                    }
                ]
                
                for sample in samples:
                    sql = text("""
                        INSERT INTO [Dividends] 
                            ([EmployeeID], [DividendAmount], [DividendDate])
                        VALUES (:emp_id, :amount, :date)
                    """)
                    conn.execute(sql, sample)
                
                print(f"   ✅ Đã tạo {len(samples)} thưởng mẫu")
                
    except Exception as e:
        print(f"   ⚠️ Lỗi tạo dữ liệu: {e}")
        print("   💡 Có thể dữ liệu đã tồn tại")
    
    # 4. Hiển thị dữ liệu
    print("\n4️⃣ Danh sách thưởng hiện tại:")
    try:
        with engine.connect() as conn:
            sql = text("""
                SELECT 
                    D.DividendID,
                    D.EmployeeID,
                    E.FullName,
                    D.DividendAmount,
                    D.DividendDate,
                    D.CreatedAt
                FROM [Dividends] D
                INNER JOIN [Employees] E ON D.EmployeeID = E.EmployeeID
                ORDER BY D.DividendDate DESC
            """)
            result = conn.execute(sql)
            dividends = result.fetchall()
            
            if dividends:
                print(f"\n   📊 Tổng: {len(dividends)} thưởng\n")
                print("   " + "-" * 90)
                print(f"   {'ID':<5} {'EmpID':<8} {'Tên':<20} {'Số tiền':<15} {'Ngày':<12} {'Tạo lúc':<20}")
                print("   " + "-" * 90)
                
                for d in dividends:
                    amount_str = f"{d[3]:,.0f} VND"
                    created = str(d[5])[:19] if d[5] else "-"
                    print(f"   {d[0]:<5} {d[1]:<8} {d[2]:<20} {amount_str:<15} {str(d[4]):<12} {created:<20}")
                
                print("   " + "-" * 90)
            else:
                print("   ⚠️ Chưa có thưởng nào")
                
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")
    
    # 5. Thống kê
    print("\n5️⃣ Thống kê:")
    try:
        with engine.connect() as conn:
            sql = text("""
                SELECT 
                    COUNT(*) as TotalDividends,
                    SUM(DividendAmount) as TotalAmount,
                    AVG(DividendAmount) as AverageAmount
                FROM [Dividends]
            """)
            result = conn.execute(sql)
            stats = result.fetchone()
            
            print(f"   📈 Tổng thưởng: {stats[0]}")
            print(f"   💰 Tổng tiền: {stats[1]:,.0f} VND")
            print(f"   📊 Trung bình: {stats[2]:,.0f} VND")
            
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")
    
    print("\n" + "=" * 60)
    print("✅ HOÀN TẤT TEST!")
    print("=" * 60)
    print("\n💡 Bước tiếp theo:")
    print("   1. Chạy backend: python app.py")
    print("   2. Test API: Mở BE/https/dividends.http")
    print("   3. Hoặc test frontend: npm run dev")
    print()

if __name__ == "__main__":
    test_dividends()
