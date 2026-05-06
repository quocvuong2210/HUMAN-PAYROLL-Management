"""
Kiểm tra cấu trúc bảng Dividends
"""
from sqlalchemy import create_engine, text
from config import SQL_SERVER_CONN

engine = create_engine(SQL_SERVER_CONN)

print("=" * 60)
print("🔍 KIỂM TRA CẤU TRÚC BẢNG DIVIDENDS")
print("=" * 60)

with engine.connect() as conn:
    # Lấy cấu trúc bảng
    sql = text("""
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            CHARACTER_MAXIMUM_LENGTH,
            IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'Dividends'
        ORDER BY ORDINAL_POSITION
    """)
    
    result = conn.execute(sql)
    columns = result.fetchall()
    
    print("\n📊 Các cột trong bảng Dividends:\n")
    print(f"{'Tên Cột':<25} {'Kiểu':<15} {'Độ dài':<10} {'Null?':<10}")
    print("-" * 60)
    
    for col in columns:
        length = str(col[2]) if col[2] else "-"
        print(f"{col[0]:<25} {col[1]:<15} {length:<10} {col[3]:<10}")
    
    print("-" * 60)
    print(f"\nTổng: {len(columns)} cột")

print("\n" + "=" * 60)
