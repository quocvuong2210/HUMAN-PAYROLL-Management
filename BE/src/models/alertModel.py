from sqlalchemy import create_engine, text
from config import MYSQL_CONN, SQL_SERVER_CONN 

class AlertModel: 
    def __init__(self, db_type="mysql"):
        if db_type == "mssql":
            self.engine = create_engine(SQL_SERVER_CONN)
        else:
            self.engine = create_engine(MYSQL_CONN)

    def execute_query(self, sql, params=None, fetch=False):
        params = params or {}
        with self.engine.connect() as conn:
            result = conn.execute(text(sql), params)
            if fetch:
                # Chuyển đổi result set thành list của các dictionary
                return [dict(row._mapping) for row in result.fetchall()]
            conn.commit()
            return result.rowcount

    # --- MSSQL: Birthdays & Anniversaries ---
    def get_birthdays(self, month=None):
        sql = """
            SELECT e.EmployeeID, e.FullName, e.DateOfBirth, e.PhoneNumber, 
                   d.DepartmentName, p.PositionName, DAY(e.DateOfBirth) as BirthDay
            FROM dbo.Employees e
            LEFT JOIN dbo.Departments d ON e.DepartmentID = d.DepartmentID
            LEFT JOIN dbo.Positions p ON e.PositionID = p.PositionID
            WHERE e.Status = N'Đang làm việc' AND (:month IS NULL OR MONTH(e.DateOfBirth) = :month)
            ORDER BY BirthDay ASC
        """
        return self.execute_query(sql, {"month": month}, True)

    def get_work_anniversaries(self, month=None):
        sql = """
            SELECT e.EmployeeID, e.FullName, e.HireDate, d.DepartmentName, p.PositionName,
                   DATEDIFF(YEAR, e.HireDate, GETDATE()) as YearsActive
            FROM dbo.Employees e
            LEFT JOIN dbo.Departments d ON e.DepartmentID = d.DepartmentID
            LEFT JOIN dbo.Positions p ON e.PositionID = p.PositionID
            WHERE e.Status = N'Đang làm việc' AND YEAR(e.HireDate) < YEAR(GETDATE())
            AND (:month IS NULL OR MONTH(e.HireDate) = :month)
            ORDER BY DAY(e.HireDate) ASC
        """
        return self.execute_query(sql, {"month": month}, True)

    # --- MYSQL: Absence, Salary, Attendance ---
    # ĐÃ XÓA e.Email Ở ĐÂY ĐỂ TRÁNH LỖI 1054
    def get_high_absenteeism(self, month=None, year=None):
        sql = """
            SELECT e.EmployeeID, e.FullName, d.DepartmentName, pos.PositionName,
                   a.WorkDays, a.AbsentDays, a.LeaveDays, (a.AbsentDays + a.LeaveDays) as TotalOff, a.AttendanceMonth
            FROM attendance a
            JOIN employees_payroll e ON a.EmployeeID = e.EmployeeID
            JOIN departments_payroll d ON e.DepartmentID = d.DepartmentID
            JOIN positions_payroll pos ON e.PositionID = pos.PositionID
            WHERE (a.AbsentDays + a.LeaveDays) > 3
            AND (:month IS NULL OR MONTH(a.AttendanceMonth) = :month)
            AND (:year IS NULL OR YEAR(a.AttendanceMonth) = :year)
        """
        return self.execute_query(sql, {"month": month, "year": year}, True)

    def get_unusual_salaries(self, month=None, year=None):
        sql = """
            SELECT e.EmployeeID, e.FullName, d.DepartmentName, pos.PositionName,
                   s.BaseSalary, s.Bonus, s.Deductions, s.NetSalary, s.SalaryMonth
            FROM salaries s
            JOIN employees_payroll e ON s.EmployeeID = e.EmployeeID
            JOIN departments_payroll d ON e.DepartmentID = d.DepartmentID
            JOIN positions_payroll pos ON e.PositionID = pos.PositionID
            WHERE (s.Deductions > (s.BaseSalary * 0.2) OR s.NetSalary > 50000000)
            AND (:month IS NULL OR MONTH(s.SalaryMonth) = :month)
            AND (:year IS NULL OR YEAR(s.SalaryMonth) = :year)
        """
        return self.execute_query(sql, {"month": month, "year": year}, True)

    def get_missing_attendance(self, month=None, year=None):
        sql = """
            SELECT e.EmployeeID, e.FullName, e.Status, d.DepartmentName
            FROM employees_payroll e
            JOIN departments_payroll d ON e.DepartmentID = d.DepartmentID
            LEFT JOIN attendance a ON e.EmployeeID = a.EmployeeID 
                AND (:month IS NULL OR MONTH(a.AttendanceMonth) = :month)
                AND (:year IS NULL OR YEAR(a.AttendanceMonth) = :year)
            WHERE e.Status != 'Đã nghỉ việc' AND a.EmployeeID IS NULL
        """
        return self.execute_query(sql, {"month": month, "year": year}, True)

    def get_employee_details(self, employee_id):
        # Sử dụng e.* để lấy các cột hiện có, đảm bảo join đúng bảng
        info_sql = """
            SELECT e.*, d.DepartmentName, p.PositionName 
            FROM employees_payroll e 
            JOIN departments_payroll d ON e.DepartmentID = d.DepartmentID 
            JOIN positions_payroll p ON e.PositionID = p.PositionID 
            WHERE e.EmployeeID = :emp_id
        """
        info = self.execute_query(info_sql, {"emp_id": employee_id}, True)
        if not info: return None
        
        res = info[0]
        # Lấy lịch sử 5 tháng gần nhất
        res['salary_history'] = self.execute_query("SELECT SalaryMonth, BaseSalary, Bonus, Deductions, NetSalary FROM salaries WHERE EmployeeID = :id ORDER BY SalaryMonth DESC LIMIT 5", {"id": employee_id}, True)
        res['attendance_history'] = self.execute_query("SELECT AttendanceMonth, WorkDays, AbsentDays, LeaveDays FROM attendance WHERE EmployeeID = :id ORDER BY AttendanceMonth DESC LIMIT 5", {"id": employee_id}, True)
        return res