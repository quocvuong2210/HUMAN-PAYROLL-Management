from sqlalchemy import create_engine, text
from config import MYSQL_CONN, SQL_SERVER_CONN
from datetime import datetime

class EmployeeModel:
    def __init__(self):
        # MSSQL: Chứa Employees, Departments, Positions (Dữ liệu gốc)
        self.mssql_engine = create_engine(SQL_SERVER_CONN)
        # MySQL: Chứa bảng payroll, salaries, attendance (Dữ liệu bổ trợ)
        self.mysql_engine = create_engine(MYSQL_CONN)

    # --- HÀM TIỆN ÍCH ---
    def execute_mssql(self, sql, params=None, fetch=False):
        with self.mssql_engine.connect() as conn:
            result = conn.execute(text(sql), params or {})
            if fetch:
                return [dict(row._mapping) for row in result.fetchall()]
            conn.commit()
            return result.rowcount

    def execute_mysql(self, sql, params=None, fetch=False):
        with self.mysql_engine.connect() as conn:
            result = conn.execute(text(sql), params or {})
            if fetch:
                return [dict(row._mapping) for row in result.fetchall()]
            conn.commit()
            return result.rowcount
    
    # --- 1. LẤY DANH SÁCH NHÂN VIÊN (BỘ LỌC ĐẦY ĐỦ + PHÂN TRANG) ---
    def get_employees_paged(self, page=1, limit=10, name=None, dept_id=None, 
                            pos_id=None, status=None, gender=None, 
                            start_date=None, end_date=None):
        """
        Lọc theo: Tên, Phòng ban, Chức vụ, Trạng thái, Giới tính, Khoảng ngày vào làm
        """
        offset = (page - 1) * limit
        
        # Xây dựng điều kiện WHERE động dựa trên các bộ lọc có dữ liệu
        where_clauses = ["1=1"]
        params = {
            "name": f"%{name}%" if name else None,
            "dept_id": dept_id,
            "pos_id": pos_id,
            "status": status,
            "gender": gender,
            "start_date": start_date,
            "end_date": end_date
        }

        if name:       where_clauses.append("e.FullName LIKE :name")
        if dept_id:    where_clauses.append("e.DepartmentID = :dept_id")
        if pos_id:     where_clauses.append("e.PositionID = :pos_id")
        if status:     where_clauses.append("e.Status = :status")
        if gender:     where_clauses.append("e.Gender = :gender")
        if start_date: where_clauses.append("e.HireDate >= :start_date")
        if end_date:   where_clauses.append("e.HireDate <= :end_date")

        where_sql = " AND ".join(where_clauses)

        # Truy vấn đếm tổng số bản ghi (dùng để tính tổng số trang)
        count_sql = f"SELECT COUNT(*) as total FROM Employees e WHERE {where_sql}"
        
        # Truy vấn lấy dữ liệu chi tiết kèm JOIN tên phòng/chức vụ
        data_sql = f"""
            SELECT e.*, d.DepartmentName, p.PositionName 
            FROM Employees e
            LEFT JOIN Departments d ON e.DepartmentID = d.DepartmentID
            LEFT JOIN Positions p ON e.PositionID = p.PositionID
            WHERE {where_sql}
            ORDER BY e.CreatedAt DESC
            OFFSET {offset} ROWS FETCH NEXT {limit} ROWS ONLY
        """
        
        total_data = self.execute_mssql(count_sql, params, fetch=True)
        total = total_data[0]['total'] if total_data else 0
        data = self.execute_mssql(data_sql, params, fetch=True)
        
        return {
            "total_records": total,
            "total_pages": (total + limit - 1) // limit,
            "current_page": page,
            "limit": limit,
            "data": data
        }

    # --- 2. THÊM MỚI NHÂN VIÊN ---
    # --- 2. THÊM MỚI NHÂN VIÊN ---
    def create_employee(self, data):
        try:
            # Thêm SET NOCOUNT ON để tránh lỗi "This result object does not return rows"
            sql_mssql = """
                SET NOCOUNT ON; 
                INSERT INTO Employees (FullName, DateOfBirth, Gender, PhoneNumber, Email, HireDate, 
                                      DepartmentID, PositionID, Status, CreatedAt)
                VALUES (:FullName, :DateOfBirth, :Gender, :PhoneNumber, :Email, :HireDate, 
                        :DepartmentID, :PositionID, :Status, GETDATE());
                SELECT SCOPE_IDENTITY() AS EmployeeID;
            """
            
            with self.mssql_engine.connect() as conn:
                # Thực thi và lấy ID ngay lập tức
                result = conn.execute(text(sql_mssql), data)
                new_id = result.fetchone()[0] # Dùng fetchone() thay cho scalar() để chắc chắn hơn
                conn.commit()

            if new_id:
                sync_payload = {
                    "EmployeeID": new_id,
                    "FullName": data['FullName'],
                    "DepartmentID": data['DepartmentID'],
                    "PositionID": data['PositionID'],
                    "Status": data.get('Status', 'Đang làm việc')
                }
                self._sync_to_mysql(sync_payload)
            
            return new_id
            
        except Exception as e:
            print(f"DATABASE ERROR: {str(e)}")
            raise e
    # --- 3. CẬP NHẬT NHÂN VIÊN ---
    def update_employee(self, emp_id, data):
        data['emp_id'] = emp_id
        sql_mssql = """
            UPDATE Employees SET 
                FullName = :FullName, DateOfBirth = :DateOfBirth, Gender = :Gender,
                PhoneNumber = :PhoneNumber, Email = :Email, DepartmentID = :DepartmentID, 
                PositionID = :PositionID, Status = :Status, UpdatedAt = GETDATE()
            WHERE EmployeeID = :emp_id
        """
        self.execute_mssql(sql_mssql, data)
        
        # Cập nhật bản sao đồng bộ bên MySQL
        self._sync_to_mysql({
            "EmployeeID": emp_id,
            "FullName": data['FullName'],
            "DepartmentID": data['DepartmentID'],
            "PositionID": data['PositionID'],
            "Status": data['Status']
        })
        return True

    # --- 4. CHI TIẾT ĐẦY ĐỦ (Hồ sơ MSSQL + Lương/Công MySQL) ---
    def get_full_employee_info(self, emp_id):
        profile = self.execute_mssql("""
            SELECT e.*, d.DepartmentName, p.PositionName 
            FROM Employees e
            LEFT JOIN Departments d ON e.DepartmentID = d.DepartmentID
            LEFT JOIN Positions p ON e.PositionID = p.PositionID
            WHERE e.EmployeeID = :id
        """, {"id": emp_id}, fetch=True)
        
        if not profile: return None
        res = profile[0]

        # Lấy lịch sử 12 tháng gần nhất từ MySQL
        res['salary_history'] = self.execute_mysql(
            "SELECT * FROM salaries WHERE EmployeeID = :id ORDER BY SalaryMonth DESC LIMIT 12",
            {"id": emp_id}, fetch=True
        )
        res['attendance_history'] = self.execute_mysql(
            "SELECT * FROM attendance WHERE EmployeeID = :id ORDER BY AttendanceMonth DESC LIMIT 12",
            {"id": emp_id}, fetch=True
        )
        return res

    # --- 5. XÓA SẠCH DỮ LIỆU (Cả 2 DB) ---
    def delete_employee_complete(self, emp_id):
        params = {"id": emp_id}
        # Xóa MySQL trước do là dữ liệu phụ thuộc
        self.execute_mysql("DELETE FROM salaries WHERE EmployeeID = :id", params)
        self.execute_mysql("DELETE FROM attendance WHERE EmployeeID = :id", params)
        self.execute_mysql("DELETE FROM employees_payroll WHERE EmployeeID = :id", params)
        # Cuối cùng xóa MSSQL
        return self.execute_mssql("DELETE FROM Employees WHERE EmployeeID = :id", params)

    # --- HÀM HỖ TRỢ ĐỒNG BỘ NỘI BỘ ---
    def _sync_to_mysql(self, sync_data):
        sql = """
            INSERT INTO employees_payroll (EmployeeID, FullName, DepartmentID, PositionID, Status, SyncedAt)
            VALUES (:EmployeeID, :FullName, :DepartmentID, :PositionID, :Status, NOW())
            AS new_data -- Dùng alias để tránh lỗi cú pháp MySQL mới
            ON DUPLICATE KEY UPDATE 
                FullName = new_data.FullName, 
                DepartmentID = new_data.DepartmentID,
                PositionID = new_data.PositionID, 
                Status = new_data.Status, 
                SyncedAt = NOW()
        """
        self.execute_mysql(sql, sync_data)
    # --- 6. ĐỒNG BỘ NHÂN VIÊN CHƯA CÓ BÊN MYSQL (BATCH SYNC) ---
    def sync_missing_employees(self):
        """
        Tìm và đồng bộ tất cả nhân viên từ MSSQL sang MySQL nếu bên MySQL chưa tồn tại.
        """
        try:
            # 1. Lấy danh sách ID hiện có bên MySQL để so sánh
            existing_mysql = self.execute_mysql("SELECT EmployeeID FROM employees_payroll", fetch=True)
            mysql_ids = [row['EmployeeID'] for row in existing_mysql]

            # 2. Lấy dữ liệu từ MSSQL (chỉ lấy các trường cần thiết để sync)
            mssql_data = self.execute_mssql("""
                SELECT EmployeeID, FullName, DepartmentID, PositionID, Status 
                FROM Employees
            """, fetch=True)

            # 3. Lọc ra những người có ở MSSQL nhưng chưa có ở MySQL
            missing_data = [emp for emp in mssql_data if emp['EmployeeID'] not in mysql_ids]

            if not missing_data:
                return {"status": "success", "message": "Dữ liệu đã đồng bộ hoàn toàn.", "synced_count": 0}

            # 4. Thực hiện Insert hàng loạt vào MySQL
            # Sử dụng cú pháp INSERT IGNORE hoặc ON DUPLICATE KEY để an toàn tuyệt đối
            sync_sql = """
                INSERT INTO employees_payroll (EmployeeID, FullName, DepartmentID, PositionID, Status, SyncedAt)
                VALUES (:EmployeeID, :FullName, :DepartmentID, :PositionID, :Status, NOW())
                ON DUPLICATE KEY UPDATE 
                    FullName = VALUES(FullName), 
                    DepartmentID = VALUES(DepartmentID),
                    PositionID = VALUES(PositionID), 
                    Status = VALUES(Status), 
                    SyncedAt = NOW()
            """
            
            # Thực thi insert từng bản ghi trong missing_data
            count = 0
            for emp in missing_data:
                self.execute_mysql(sync_sql, emp)
                count += 1

            return {
                "status": "success", 
                "message": f"Đã đồng bộ thành công {count} nhân viên mới.", 
                "synced_count": count
            }

        except Exception as e:
            print(f"Lỗi đồng bộ: {str(e)}")
            return {"status": "error", "message": str(e)}