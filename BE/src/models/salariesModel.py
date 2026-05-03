from sqlalchemy import create_engine, text
from config import MYSQL_CONN
from datetime import datetime
import pandas as pd
class SalaryModel:
    def __init__(self):
        self.mysql_engine = create_engine(MYSQL_CONN)

    def execute_query(self, sql, params=None, fetch=False):
        with self.mysql_engine.connect() as conn:
            result = conn.execute(text(sql), params or {})
            if fetch:
                return [dict(row._mapping) for row in result.fetchall()]
            conn.commit()
            return result.rowcount

    # Mapping các cột để tránh SQL Injection
    def _get_sort_query(self, sort_by, default="e.FullName", order="ASC"):
        allowed_cols = {
            "FullName": "e.FullName",
            "DepartmentName": "d.DepartmentName",
            "PositionName": "p.PositionName",
            "BaseSalary": "s.BaseSalary",
            "Bonus": "s.Bonus",
            "Deductions": "s.Deductions",
            "NetSalary": "s.NetSalary"
        }
        column = allowed_cols.get(sort_by, default)
        direction = "DESC" if str(order).upper() == "DESC" else "ASC"
        return f"ORDER BY {column} {direction}"

    # =========================================
    # 1. DANH SÁCH LƯƠNG (CÓ SẮP XẾP)
    # =========================================
    def get_salary_list(self, month=None, name=None, dept_id=None, pos_id=None, status=None, page=1, limit=10, sort_by="FullName", sort_order="ASC"):
        month = month or datetime.now().strftime('%Y-%m-01')
        offset = (page - 1) * limit
        sort_sql = self._get_sort_query(sort_by, "e.FullName", sort_order)

        filter_sql = """
            FROM employees_payroll e
            LEFT JOIN departments_payroll d ON e.DepartmentID = d.DepartmentID
            LEFT JOIN positions_payroll p ON e.PositionID = p.PositionID
            LEFT JOIN salaries s ON e.EmployeeID = s.EmployeeID 
                AND DATE_FORMAT(s.SalaryMonth, '%Y-%m') = DATE_FORMAT(:month, '%Y-%m')
            WHERE 1=1
        """
        params = {"month": month}

        if name:
            filter_sql += " AND e.FullName LIKE :name"
            params["name"] = f"%{name}%"
        if dept_id:
            filter_sql += " AND e.DepartmentID = :dept_id"
            params["dept_id"] = dept_id
        if pos_id:
            filter_sql += " AND e.PositionID = :pos_id"
            params["pos_id"] = pos_id
        if status == "calculated":
            filter_sql += " AND s.SalaryID IS NOT NULL"
        elif status == "pending":
            filter_sql += " AND s.SalaryID IS NULL"

        count_sql = f"SELECT COUNT(*) as total {filter_sql}"
        total_records = self.execute_query(count_sql, params, fetch=True)[0]['total']

        query_sql = f"""
            SELECT 
                e.EmployeeID, e.FullName, d.DepartmentName, p.PositionName,
                s.SalaryID, s.BaseSalary, s.Bonus, s.Deductions, s.NetSalary,
                CASE WHEN s.SalaryID IS NOT NULL THEN 'calculated' ELSE 'pending' END as salaryStatus
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
            "total_pages": (total_records + limit - 1) // limit if total_records > 0 else 0,
            "current_page": page
        }
    # =========================================
    # 2. TÍNH LƯƠNG VÀ LƯU VÀO DATABASE
    # =========================================
    def process_salary(self, employee_id, month, base_salary, bonus=0, deductions=0):
        net_salary = float(base_salary) + float(bonus) - float(deductions)
        
        sql = """
            INSERT INTO salaries (EmployeeID, SalaryMonth, BaseSalary, Bonus, Deductions, NetSalary, CreatedAt)
            VALUES (:eid, :month, :base, :bonus, :deduct, :net, NOW())
        """
        params = {
            "eid": employee_id,
            "month": month,
            "base": base_salary,
            "bonus": bonus,
            "deduct": deductions,
            "net": net_salary
        }
        return self.execute_query(sql, params)

    # =========================================
    # 3. CẬP NHẬT LƯƠNG
    # =========================================
    def update_salary(self, salary_id, base_salary, bonus, deductions):
        net_salary = float(base_salary) + float(bonus) - float(deductions)
        
        sql = """
            UPDATE salaries 
            SET BaseSalary = :base, Bonus = :bonus, Deductions = :deduct, NetSalary = :net
            WHERE SalaryID = :id
        """
        params = {
            "id": salary_id,
            "base": base_salary,
            "bonus": bonus,
            "deduct": deductions,
            "net": net_salary
        }
        return self.execute_query(sql, params)

    # =========================================
    # 4. LẤY CHI TIẾT LƯƠNG MỘT NHÂN VIÊN
    # =========================================
    def get_employee_salary_history(self, employee_id):
        sql = "SELECT * FROM salaries WHERE EmployeeID = :eid ORDER BY SalaryMonth DESC"
        return self.execute_query(sql, {"eid": employee_id}, fetch=True)

    # =========================================
    # 5. TÌM KIẾM THEO TRẠNG THÁI LƯƠNG (ĐÃ TÍNH / CHƯA TÍNH)
    # =========================================
    def get_salary_status_list(self, month=None, status=None, page=1, limit=10):
        month = month or datetime.now().strftime('%Y-%m-01')
        offset = (page - 1) * limit

        # status: 'calculated' (đã tính), 'pending' (chưa tính)
        filter_sql = """
            FROM employees_payroll e
            LEFT JOIN salaries s ON e.EmployeeID = s.EmployeeID 
                AND DATE_FORMAT(s.SalaryMonth, '%Y-%m') = DATE_FORMAT(:month, '%Y-%m')
            LEFT JOIN departments_payroll d ON e.DepartmentID = d.DepartmentID
            WHERE 1=1
        """
        params = {"month": month}

        if status == "calculated":
            filter_sql += " AND s.SalaryID IS NOT NULL"
        elif status == "pending":
            filter_sql += " AND s.SalaryID IS NULL"

        count_sql = f"SELECT COUNT(*) as total {filter_sql}"
        total_records = self.execute_query(count_sql, params, fetch=True)[0]['total']

        query_sql = f"""
            SELECT 
                e.EmployeeID, e.FullName, d.DepartmentName,
                s.SalaryID, s.NetSalary, s.SalaryMonth,
                CASE WHEN s.SalaryID IS NOT NULL THEN 'calculated' ELSE 'pending' END as salaryStatus
            {filter_sql}
            ORDER BY e.FullName ASC
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
    # 6. KIỂM TRA TRẠNG THÁI LƯƠNG CỦA 1 NV
    # =========================================
    def check_employee_salary_status(self, employee_id, month):
        sql = """
            SELECT SalaryID 
            FROM salaries 
            WHERE EmployeeID = :eid 
            AND DATE_FORMAT(SalaryMonth, '%Y-%m') = DATE_FORMAT(:month, '%Y-%m')
        """
        result = self.execute_query(sql, {"eid": employee_id, "month": month}, fetch=True)
        return len(result) > 0
    def get_full_payroll_data(self, month):
    # month định dạng 'YYYY-MM'
        sql = """
            SELECT 
                e.EmployeeID, 
                e.FullName, 
                d.DepartmentName, 
                p.PositionName,
                COALESCE(a.WorkDays, 0) as WorkDays,
                COALESCE(a.AbsentDays, 0) as AbsentDays,
                s.BaseSalary, 
                s.Bonus, 
                s.Deductions, 
                s.NetSalary
            FROM employees_payroll e
            LEFT JOIN departments_payroll d ON e.DepartmentID = d.DepartmentID
            LEFT JOIN positions_payroll p ON e.PositionID = p.PositionID
            LEFT JOIN attendance a ON e.EmployeeID = a.EmployeeID 
                AND DATE_FORMAT(a.AttendanceMonth, '%Y-%m') = :month
            LEFT JOIN salaries s ON e.EmployeeID = s.EmployeeID 
                AND DATE_FORMAT(s.SalaryMonth, '%Y-%m') = :month
            ORDER BY e.FullName ASC
        """
        return self.execute_query(sql, {"month": month}, fetch=True)
   

    def export_payroll_to_excel(self, month, output_file="Payroll_Report.xlsx"):
        data = self.get_full_payroll_data(month)
        if not data:
            return False
    
    # Chuyển dữ liệu thành DataFrame
        df = pd.DataFrame(data)
    
    # Đổi tên cột cho đẹp (Tiếng Việt)
        df.columns = [
        'Mã NV', 'Họ Tên', 'Phòng Ban', 'Chức Vụ', 
        'Số ngày công', 'Số ngày nghỉ', 
        'Lương cơ bản', 'Thưởng', 'Khấu trừ', 'Thực nhận'
        ]
    
    # Xuất ra file Excel
        df.to_excel(output_file, index=False)
        return True
