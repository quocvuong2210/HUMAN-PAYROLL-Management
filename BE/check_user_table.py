"""
Kiểm tra cấu trúc bảng USER
"""
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

engine = create_engine(SQL_SERVER_PERMISSION_CONN)

with engine.connect() as conn:
    # Lấy cấu trúc bảng USER
    result = conn.execute(text("""
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            CHARACTER_MAXIMUM_LENGTH,
            IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'USER'
        ORDER BY ORDINAL_POSITION
    """))
    
    print("📊 Cấu trúc bảng [USER]:")
    print("-" * 80)
    for row in result:
        print(f"  - {row[0]:<20} {row[1]:<15} {str(row[2]):<10} {'NULL' if row[3] == 'YES' else 'NOT NULL'}")
    
    # Kiểm tra có user nào không
    result = conn.execute(text("SELECT COUNT(*) FROM [USER]"))
    count = result.fetchone()[0]
    print(f"\n📈 Tổng số users: {count}")
    
    if count > 0:
        result = conn.execute(text("SELECT TOP 5 * FROM [USER]"))
        print(f"\n👥 5 users đầu tiên:")
        for row in result:
            print(f"  - {row}")
