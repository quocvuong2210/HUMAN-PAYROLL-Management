from sqlalchemy import create_engine, text
from config import MYSQL_CONN, SQL_SERVER_CONN 

class DepartmentModel: 
    def __init__(self, db_type="mysql"):
        self.db_type = db_type
        # Khởi tạo engine dựa trên loại Database được chọn
        if db_type == "mssql":
            self.engine = create_engine(SQL_SERVER_CONN)
        else:
            self.engine = create_engine(MYSQL_CONN)

    def execute_query(self, sql, params=None, fetch=False):
        """Hàm thực thi truy vấn tập trung với cơ chế Auto-Commit"""
        with self.engine.connect() as conn:
            with conn.begin():
                query = text(sql)
                result = conn.execute(query, params or {})
                
                if fetch:
                    return [dict(row._mapping) for row in result.fetchall()]
                
                return result.rowcount

    # --- TRUY VẤN DANH SÁCH TỔNG HỢP (NHÂN VIÊN + LƯƠNG) ---
    def get_departments_with_stats(self, search_name=None, sort_by="DepartmentID", order="ASC"):
        params = {}
        # Cập nhật SQL: JOIN thêm bảng salaries để lấy NetSalary hoặc BaseSalary
        sql = """
            SELECT 
                d.DepartmentID, 
                d.DepartmentName, 
                d.SyncedAt,
                COUNT(DISTINCT e.EmployeeID) AS TotalEmployees,
                IFNULL(SUM(s.NetSalary), 0) AS TotalSalary
            FROM departments_payroll d
            LEFT JOIN employees_payroll e ON d.DepartmentID = e.DepartmentID
            LEFT JOIN salaries s ON e.EmployeeID = s.EmployeeID
        """
        
        if search_name:
            sql += " WHERE d.DepartmentName LIKE :name"
            params["name"] = f"%{search_name}%"
            
        sql += " GROUP BY d.DepartmentID, d.DepartmentName, d.SyncedAt"
        
        # Kiểm tra cột sort hợp lệ
        allowed_columns = ["DepartmentID", "DepartmentName", "TotalEmployees", "TotalSalary", "SyncedAt"]
        if sort_by not in allowed_columns:
            sort_by = "DepartmentID"
        
        order = "DESC" if order.upper() == "DESC" else "ASC"
        sql += f" ORDER BY {sort_by} {order}"
        
        # Xử lý Engine
        target_engine = self.engine
        if self.db_type == "mssql":
             target_engine = create_engine(MYSQL_CONN)

        with target_engine.connect() as conn:
            query = text(sql)
            result = conn.execute(query, params)
            return [dict(row._mapping) for row in result.fetchall()]

    def get_department_by_id(self, dept_id):
        table_name = "dbo.Departments" if self.db_type == "mssql" else "departments_payroll"
        sql = f"SELECT * FROM {table_name} WHERE DepartmentID = :id"
        result = self.execute_query(sql, params={"id": dept_id}, fetch=True)
        return result[0] if result else None

    # --- THAO TÁC DỮ LIỆU ---

    def add_department_mssql(self, name):
        """Thêm vào SQL Server (Master)"""
        sql = """
            INSERT INTO dbo.Departments (DepartmentName, CreatedAt) 
            OUTPUT INSERTED.DepartmentID
            VALUES (:name, GETDATE())
        """
        return self.execute_query(sql, params={"name": name}, fetch=True)

    def add_department_mysql(self, dept_id, name):
        """Đồng bộ sang MySQL (Slave)"""
        sql = """
            INSERT INTO departments_payroll (DepartmentID, DepartmentName, SyncedAt)
            VALUES (:id, :name, NOW())
            ON DUPLICATE KEY UPDATE DepartmentName = :name, SyncedAt = NOW()
        """
        return self.execute_query(sql, params={"id": dept_id, "name": name})

    def update_department(self, dept_id, new_name):
        table_name = "dbo.Departments" if self.db_type == "mssql" else "departments_payroll"
        sql = f"UPDATE {table_name} SET DepartmentName = :name WHERE DepartmentID = :id"
        return self.execute_query(sql, params={"id": dept_id, "name": new_name})

    def delete_department(self, dept_id):
        table_name = "dbo.Departments" if self.db_type == "mssql" else "departments_payroll"
        sql = f"DELETE FROM {table_name} WHERE DepartmentID = :id"
        return self.execute_query(sql, params={"id": dept_id})

    def get_all_mssql(self):
        sql = "SELECT * FROM dbo.Departments ORDER BY DepartmentID ASC"
        if self.db_type != "mssql":
            temp_engine = create_engine(SQL_SERVER_CONN)
            with temp_engine.connect() as conn:
                result = conn.execute(text(sql))
                return [dict(row._mapping) for row in result.fetchall()]
        return self.execute_query(sql, fetch=True)