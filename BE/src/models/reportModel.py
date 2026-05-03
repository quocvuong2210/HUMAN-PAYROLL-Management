from sqlalchemy import create_engine, text
from config import MYSQL_CONN

class ReportModel:
    def __init__(self):
        self.mysql_engine = create_engine(MYSQL_CONN)

    # --- HÀM TIỆN ÍCH ---
    def execute_mysql(self, sql, params=None):
        with self.mysql_engine.connect() as conn:
            result = conn.execute(text(sql), params or {})
            return [dict(row._mapping) for row in result.fetchall()]

    def _get_date_filter(self, date_col, month, year):
        """Hàm hỗ trợ tạo chuỗi SQL và tham số lọc"""
        sql_filter = ""
        params = {}
        if month:
            sql_filter += f" AND MONTH({date_col}) = :month"
            params['month'] = month
        if year:
            sql_filter += f" AND YEAR({date_col}) = :year"
            params['year'] = year
        return sql_filter, params

    # --- CÁC BÁO CÁO CÓ LỌC ---
    
    def salary_by_department(self, month=None, year=None):
        date_filter, params = self._get_date_filter("s.SalaryMonth", month, year)
        sql = f"""
        SELECT d.DepartmentName, SUM(s.NetSalary) AS TotalSalary
        FROM salaries s
        JOIN employees_payroll e ON s.EmployeeID = e.EmployeeID
        JOIN departments_payroll d ON e.DepartmentID = d.DepartmentID
        WHERE 1=1 {date_filter}
        GROUP BY d.DepartmentName
        ORDER BY TotalSalary DESC
        """
        return self.execute_mysql(sql, params)

    def attendance_report(self, month=None, year=None):
        date_filter, params = self._get_date_filter("a.AttendanceMonth", month, year)
        sql = f"""
        SELECT e.FullName, a.WorkDays, a.AbsentDays, a.LeaveDays
        FROM attendance a
        JOIN employees_payroll e ON a.EmployeeID = e.EmployeeID
        WHERE 1=1 {date_filter}
        """
        return self.execute_mysql(sql, params)

    def payroll_detail(self, month=None, year=None):
        date_filter, params = self._get_date_filter("s.SalaryMonth", month, year)
        sql = f"""
        SELECT e.FullName, s.BaseSalary, s.Bonus, s.Deductions, s.NetSalary
        FROM salaries s
        JOIN employees_payroll e ON s.EmployeeID = e.EmployeeID
        WHERE 1=1 {date_filter}
        """
        return self.execute_mysql(sql, params)

    def alert_report(self, month=None, year=None):
        # Lọc theo tháng năm dựa trên bảng lương/chấm công
        date_filter, params = self._get_date_filter("s.SalaryMonth", month, year)
        sql = f"""
        SELECT e.FullName, a.AbsentDays, s.NetSalary
        FROM employees_payroll e
        JOIN attendance a ON e.EmployeeID = a.EmployeeID
        JOIN salaries s ON e.EmployeeID = s.EmployeeID
        WHERE (a.AbsentDays > 2 OR s.NetSalary < 6000000) {date_filter}
        """
        return self.execute_mysql(sql, params)

    # Các hàm thống kê không phụ thuộc thời gian (không cần lọc)
    def employee_distribution(self):
        sql = "SELECT Status, COUNT(*) AS Total FROM employees_payroll GROUP BY Status"
        return self.execute_mysql(sql)

    def position_report(self):
        sql = """SELECT p.PositionName, COUNT(*) AS Total 
                 FROM employees_payroll e 
                 JOIN positions_payroll p ON e.PositionID = p.PositionID 
                 GROUP BY p.PositionName"""
        return self.execute_mysql(sql)

    def department_cost(self, month=None, year=None):
        date_filter, params = self._get_date_filter("s.SalaryMonth", month, year)
        sql = f"""
        SELECT d.DepartmentName, SUM(s.NetSalary) AS TotalCost
        FROM salaries s
        JOIN employees_payroll e ON s.EmployeeID = e.EmployeeID
        JOIN departments_payroll d ON e.DepartmentID = d.DepartmentID
        WHERE 1=1 {date_filter}
        GROUP BY d.DepartmentName
        ORDER BY TotalCost DESC LIMIT 1
        """
        return self.execute_mysql(sql, params)

    def best_employee(self, month=None, year=None):
        date_filter, params = self._get_date_filter("s.SalaryMonth", month, year)
        sql = f"""
        SELECT e.FullName, (s.NetSalary / NULLIF(a.WorkDays,0)) AS SalaryPerDay
        FROM employees_payroll e
        JOIN salaries s ON e.EmployeeID = s.EmployeeID
        JOIN attendance a ON e.EmployeeID = a.EmployeeID
        WHERE 1=1 {date_filter}
        ORDER BY SalaryPerDay DESC LIMIT 1
        """
        return self.execute_mysql(sql, params)

    def dashboard(self, month=None, year=None):
        """Dashboard tổng hợp có áp dụng bộ lọc"""
        return {
            "salaryByDept": self.salary_by_department(month, year),
            "employeeDistribution": self.employee_distribution(),
            "positionReport": self.position_report(),
            "attendanceReport": self.attendance_report(month, year),
            "payrollDetail": self.payroll_detail(month, year),
            "alertReport": self.alert_report(month, year),
            "topDepartment": self.department_cost(month, year),
            "bestEmployee": self.best_employee(month, year)
        }