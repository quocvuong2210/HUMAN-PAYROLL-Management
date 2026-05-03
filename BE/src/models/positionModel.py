from sqlalchemy import create_engine, text
from config import MYSQL_CONN, SQL_SERVER_CONN

class PositionModel:
    def __init__(self, db_type="mysql"):
        self.db_type = db_type
        # Khởi tạo engine dựa trên loại Database được chọn
        if db_type == "mssql":
            self.engine = create_engine(SQL_SERVER_CONN)
        else:
            self.engine = create_engine(MYSQL_CONN)

    def execute_query(self, sql, params=None, fetch=False):
        """Hàm thực thi truy vấn tập trung"""
        with self.engine.connect() as conn:
            with conn.begin():
                query = text(sql)
                result = conn.execute(query, params or {})
                if fetch:
                    return [dict(row._mapping) for row in result.fetchall()]
                return result.rowcount

    # --- TRUY VẤN TỔNG HỢP (READ) ---

    def get_positions(self, search_name=None):
        """
        Lấy danh sách chức vụ kèm theo tổng số nhân viên (TotalEmployees).
        Sử dụng LEFT JOIN với bảng employees_payroll để đếm.
        """
        params = {}
        # Câu lệnh SQL tính toán thống kê
        sql = """
            SELECT 
                p.PositionID, 
                p.PositionName, 
                p.SyncedAt,
                COUNT(e.EmployeeID) AS TotalEmployees
            FROM positions_payroll p
            LEFT JOIN employees_payroll e ON p.PositionID = e.PositionID
        """
        
        if search_name:
            sql += " WHERE p.PositionName LIKE :name"
            params["name"] = f"%{search_name}%"
            
        sql += " GROUP BY p.PositionID, p.PositionName, p.SyncedAt"
        sql += " ORDER BY p.PositionID ASC"

        # Đảm bảo logic thống kê luôn chạy trên MySQL (Slave)
        target_engine = self.engine
        if self.db_type == "mssql":
            # Tạo engine tạm thời kết nối tới MySQL nếu instance hiện tại là MSSQL
            target_engine = create_engine(MYSQL_CONN)

        try:
            with target_engine.connect() as conn:
                query = text(sql)
                result = conn.execute(query, params)
                return [dict(row._mapping) for row in result.fetchall()]
        except Exception as e:
            print(f"Lỗi truy vấn Position stats: {e}")
            return []

    def get_position_by_id(self, pos_id):
        """Lấy chi tiết 1 chức vụ"""
        table_name = "dbo.Positions" if self.db_type == "mssql" else "positions_payroll"
        sql = f"SELECT * FROM {table_name} WHERE PositionID = :id"
        result = self.execute_query(sql, params={"id": pos_id}, fetch=True)
        return result[0] if result else None

    # --- ĐỒNG BỘ CUD (CREATE - UPDATE - DELETE) ---

    def add_position_mssql(self, name):
        """Thêm vào SQL Server (Master) và trả về ID vừa tạo"""
        sql = """
            INSERT INTO dbo.Positions (PositionName, CreatedAt) 
            OUTPUT INSERTED.PositionID
            VALUES (:name, GETDATE())
        """
        return self.execute_query(sql, params={"name": name}, fetch=True)

    def add_position_mysql(self, pos_id, name):
        """Đồng bộ dữ liệu sang MySQL (Slave)"""
        sql = """
            INSERT INTO positions_payroll (PositionID, PositionName, SyncedAt)
            VALUES (:id, :name, NOW())
            ON DUPLICATE KEY UPDATE 
                PositionName = :name, 
                SyncedAt = NOW()
        """
        return self.execute_query(sql, params={"id": pos_id, "name": name})

    def update_position(self, pos_id, new_name):
        """Cập nhật tên chức vụ"""
        if self.db_type == "mssql":
            sql = "UPDATE dbo.Positions SET PositionName = :name, UpdatedAt = GETDATE() WHERE PositionID = :id"
        else:
            sql = "UPDATE positions_payroll SET PositionName = :name, SyncedAt = NOW() WHERE PositionID = :id"
            
        return self.execute_query(sql, params={"id": pos_id, "name": new_name})

    def delete_position(self, pos_id):
        """Xóa chức vụ"""
        table_name = "dbo.Positions" if self.db_type == "mssql" else "positions_payroll"
        sql = f"DELETE FROM {table_name} WHERE PositionID = :id"
        return self.execute_query(sql, params={"id": pos_id})

    def get_all_mssql(self):
        """Lấy toàn bộ dữ liệu từ Master để phục vụ tính năng Sync thủ công"""
        sql = "SELECT PositionID, PositionName FROM dbo.Positions"
        # Nếu đang ở engine MySQL, phải kết nối thủ công sang MSSQL
        if self.db_type != "mssql":
            temp_engine = create_engine(SQL_SERVER_CONN)
            with temp_engine.connect() as conn:
                result = conn.execute(text(sql))
                return [dict(row._mapping) for row in result.fetchall()]
        return self.execute_query(sql, fetch=True)