from sqlalchemy import create_engine, text
from config import MYSQL_CONN
from datetime import datetime

class AttendanceModel:
    def __init__(self):
        self.mysql_engine = create_engine(MYSQL_CONN)

    def execute_query(self, sql, params=None, fetch=False):
        with self.mysql_engine.connect() as conn:
            result = conn.execute(text(sql), params or {})
            if fetch:
                return [dict(row._mapping) for row in result.fetchall()]
            conn.commit()
            return result.rowcount

    # =========================================
    # 1. DANH SÁCH CHẤM CÔNG (FULL FILTER)
    # ========================================
    # Hàm trợ giúp tạo chuỗi ORDER BY an toàn
    def _get_sort_query(self, sort_by, default="e.FullName", order="ASC"):
        allowed_cols = {
            "FullName": "e.FullName",
            "DepartmentName": "d.DepartmentName",
            "PositionName": "p.PositionName",
            "WorkDays": "COALESCE(a.WorkDays, 0)",
            "AbsentDays": "COALESCE(a.AbsentDays, 0)",
            "LeaveDays": "COALESCE(a.LeaveDays, 0)"
        }
        column = allowed_cols.get(sort_by, default)
        direction = "DESC" if str(order).upper() == "DESC" else "ASC"
        return f"ORDER BY {column} {direction}"

    # =========================================
    # 1. DANH SÁCH CHẤM CÔNG (CÓ SẮP XẾP)
    # =========================================
    def get_full_attendance_list(
        self, month=None, name=None, dept_id=None, pos_id=None, 
        status=None, page=1, limit=10, sort_by="FullName", sort_order="ASC"
    ):
        month = month or datetime.now().strftime('%Y-%m-01')
        offset = (page - 1) * limit
        sort_sql = self._get_sort_query(sort_by, "e.FullName", sort_order)

        filter_sql = """
            FROM employees_payroll e
            LEFT JOIN departments_payroll d ON e.DepartmentID = d.DepartmentID
            LEFT JOIN positions_payroll p ON e.PositionID = p.PositionID
            LEFT JOIN attendance a ON e.EmployeeID = a.EmployeeID 
                AND DATE_FORMAT(a.AttendanceMonth, '%Y-%m') = DATE_FORMAT(:month, '%Y-%m')
            WHERE 1=1
        """
        params = {"month": month}

        # --- Xây dựng điều kiện lọc ---
        if name:
            filter_sql += " AND e.FullName LIKE :name"
            params["name"] = f"%{name}%"
        if dept_id:
            filter_sql += " AND e.DepartmentID = :dept_id"
            params["dept_id"] = dept_id
        if pos_id:
            filter_sql += " AND e.PositionID = :pos_id"
            params["pos_id"] = pos_id
        if status is not None and status != "":
            if status in ["1", "recorded"]:
                filter_sql += " AND a.AttendanceID IS NOT NULL"
            elif status in ["0", "missing"]:
                filter_sql += " AND a.AttendanceID IS NULL"

        count_sql = f"SELECT COUNT(*) as total {filter_sql}"
        total_records = self.execute_query(count_sql, params, fetch=True)[0]['total']

        # --- Lấy dữ liệu với ORDER BY động ---
        query_sql = f"""
            SELECT 
                e.EmployeeID, e.FullName, d.DepartmentName, p.PositionName,
                a.AttendanceID,
                COALESCE(a.WorkDays, 0) as WorkDays,
                COALESCE(a.AbsentDays, 0) as AbsentDays,
                COALESCE(a.LeaveDays, 0) as LeaveDays,
                CASE WHEN a.AttendanceID IS NOT NULL THEN 1 ELSE 0 END as isRecorded
            {filter_sql}
            {sort_sql}
            LIMIT :limit OFFSET :offset
        """
        params["limit"] = limit
        params["offset"] = offset

        data = self.execute_query(query_sql, params, fetch=True)
        
        return {
            "data": data,
            "total_records": total_records,
            "total_pages": (total_records + limit - 1) // limit,
            "current_page": page
        }
    # =========================================
    # 2. CHECK CHẤM CÔNG
    # =========================================
    def check_attendance_exists(self, employee_id, month):
        sql = """
            SELECT 1 FROM attendance 
            WHERE EmployeeID = :emp_id 
            AND DATE_FORMAT(AttendanceMonth, '%Y-%m') = DATE_FORMAT(:month, '%Y-%m')
        """
        result = self.execute_query(sql, {
            "emp_id": employee_id,
            "month": month
        }, fetch=True)

        return len(result) > 0

    # =========================================
    # 3. CHECK NHÂN VIÊN
    # =========================================
    def check_employee_exists(self, employee_id):
        sql = "SELECT 1 FROM employees_payroll WHERE EmployeeID = :id"
        result = self.execute_query(sql, {"id": employee_id}, fetch=True)
        return len(result) > 0

    # =========================================
    # 4. INSERT
    # =========================================
    def insert_attendance(self, data):
        sql = """
            INSERT INTO attendance 
            (
                EmployeeID, 
                WorkDays, 
                AbsentDays, 
                LeaveDays, 
                AttendanceMonth, 
                CreatedAt
            )
            VALUES 
            (
                :EmployeeID, 
                :WorkDays, 
                :AbsentDays, 
                :LeaveDays, 
                :AttendanceMonth, 
                NOW()
            )
        """
        return self.execute_query(sql, data)

    # =========================================
    # 5. UPDATE
    # =========================================
    def update_attendance(self, attendance_id, data):
        sql = """
            UPDATE attendance 
            SET 
                WorkDays = :WorkDays, 
                AbsentDays = :AbsentDays, 
                LeaveDays = :LeaveDays
            WHERE AttendanceID = :id
        """

        params = {
            "id": attendance_id,
            "WorkDays": data.get("WorkDays", 0),
            "AbsentDays": data.get("AbsentDays", 0),
            "LeaveDays": data.get("LeaveDays", 0)
        }

        return self.execute_query(sql, params)

    # =========================================
    # 6. NHÂN VIÊN CHƯA CHẤM (THEO THÁNG)
    # =========================================
    def get_missing_attendance(self, month=None, name=None, dept_id=None):
        month = month or datetime.now().strftime('%Y-%m-01')

        sql = """
            SELECT 
                e.EmployeeID, 
                e.FullName, 
                d.DepartmentName
            FROM employees_payroll e
            LEFT JOIN departments_payroll d 
                ON e.DepartmentID = d.DepartmentID
            LEFT JOIN attendance a 
                ON e.EmployeeID = a.EmployeeID 
                AND DATE_FORMAT(a.AttendanceMonth, '%Y-%m') = DATE_FORMAT(:month, '%Y-%m')
            WHERE a.AttendanceID IS NULL
        """

        params = {"month": month}

        if name:
            sql += " AND e.FullName LIKE :name"
            params["name"] = f"%{name}%"

        if dept_id:
            sql += " AND e.DepartmentID = :dept_id"
            params["dept_id"] = dept_id

        sql += " ORDER BY e.FullName ASC"

        return self.execute_query(sql, params, fetch=True)