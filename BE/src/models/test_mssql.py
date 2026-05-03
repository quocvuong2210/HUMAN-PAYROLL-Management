from src.models.departmentModel import DepartmentModel

def check_data():
    # Khởi tạo với db_type="mssql"
    model = DepartmentModel(db_type="mssql")
    
    print("--- ĐANG LẤY DỮ LIỆU TỪ SQL SERVER ---")
    data = model.get_all_mssql()
    
    if not data:
        print("Bảng dbo.Departments trên SQL Server hiện đang trống!")
    else:
        for item in data:
            print(f"ID: {item['DepartmentID']} | Name: {item['DepartmentName']} | CreatedAt: {item['CreatedAt']}")

if __name__ == "__main__":
    check_data()