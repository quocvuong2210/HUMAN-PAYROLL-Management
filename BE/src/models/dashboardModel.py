from sqlalchemy import create_engine, text
from config import MYSQL_CONN, SQL_SERVER_CONN 

class DashboardModel: 
    def __init__(self, db_type="mysql"):
        if db_type == "mssql":
            self.engine = create_engine(SQL_SERVER_CONN)
        else:
            self.engine = create_engine(MYSQL_CONN)

    def execute_query(self, sql, params=None, fetch=False):
        with self.engine.connect() as conn:
            query = text(sql)
            result = conn.execute(query, params or {})
            
            if fetch:
                return [dict(row._mapping) for row in result.fetchall()]
            
            conn.commit()
            return result.rowcount

    # --- QUẢN LÝ NHÂN VIÊN & LƯƠNG CƠ BẢN ---
    # Tổng số nhân viên
    def get_total_employees(self):
        sql = "SELECT COUNT(*) as Total FROM Employees"
        result = self.execute_query(sql, fetch=True)
        return result[0]['Total'] if result else 0
    def get_total_departments(self):
        sql = "SELECT COUNT(*) as Total FROM Departments"
        result = self.execute_query(sql, fetch=True)
        return result[0]['Total'] if result else 0
   

    
    def get_payroll_stats(self, month=None, year=None):
        filters = []
        params = {}
        if year:
            filters.append("YEAR(SalaryMonth) = :year")
            params["year"] = year
        if month:
            filters.append("MONTH(SalaryMonth) = :month")
            params["month"] = month

        where_clause = "WHERE " + " AND ".join(filters) if filters else ""

        sql = f"""
            SELECT 
                COALESCE(SUM(NetSalary), 0) as TotalNetSalary,
                COALESCE(SUM(Bonus), 0) as TotalBonus,
                COALESCE(SUM(Deductions), 0) as TotalDeductions,
                COUNT(DISTINCT EmployeeID) as EmployeesPaid
            FROM salaries 
            {where_clause}
        """
        result = self.execute_query(sql, params=params, fetch=True)
        return result[0] if result else {"TotalNetSalary": 0, "TotalBonus": 0, "TotalDeductions": 0, "EmployeesPaid": 0}
    # --- DỮ LIỆU BIỂU ĐỒ ---

    def get_salary_by_department(self, month=None, year=2026):
        """Biểu đồ cột: Lương theo phòng ban (Tháng hoặc Năm)"""
        month_filter = "AND MONTH(s.SalaryMonth) = :month" if month else ""
        sql = f"""
            SELECT d.DepartmentName, SUM(s.NetSalary) as TotalSalary
            FROM departments_payroll d
            JOIN employees_payroll e ON d.DepartmentID = e.DepartmentID
            JOIN salaries s ON e.EmployeeID = s.EmployeeID
            WHERE YEAR(s.SalaryMonth) = :year {month_filter}
            GROUP BY d.DepartmentName
        """
        return self.execute_query(sql, params={"year": year, "month": month}, fetch=True)

    def get_salary_trend(self, year=2026):
        """Biểu đồ đường: Xu hướng lương 12 tháng trong năm"""
        sql = """
            SELECT MONTH(SalaryMonth) as Month, SUM(NetSalary) as TotalSalary
            FROM salaries
            WHERE YEAR(SalaryMonth) = :year
            GROUP BY Month
            ORDER BY Month ASC
        """
        return self.execute_query(sql, params={"year": year}, fetch=True)

    def get_employee_status_distribution(self):
        """Biểu đồ tròn: Tỷ lệ trạng thái nhân viên hiện tại"""
        sql = "SELECT Status, COUNT(*) as Count FROM employees_payroll GROUP BY Status"
        return self.execute_query(sql, fetch=True)

    # --- THỐNG KÊ CHUYÊN CẦN (ATTENDANCE) ---

    def get_avg_workdays(self, month=None, year=2026):
        month_filter = "AND MONTH(AttendanceMonth) = :month" if month else ""
        sql = f"""
            SELECT AVG(WorkDays) as AvgWorkDays 
            FROM attendance 
            WHERE YEAR(AttendanceMonth) = :year {month_filter}
        """
        result = self.execute_query(sql, params={"month": month, "year": year}, fetch=True)
        return result[0]['AvgWorkDays'] if result and result[0]['AvgWorkDays'] else 0

    def get_top_diligent_employees(self, month=None, year=2026):
        """Top 5 nhân viên đi làm nhiều nhất (Cộng dồn nếu lọc theo năm)"""
        month_filter = "AND MONTH(a.AttendanceMonth) = :month" if month else ""
        sql = f"""
            SELECT e.FullName, SUM(a.WorkDays) as WorkDays
            FROM attendance a
            JOIN employees_payroll e ON a.EmployeeID = e.EmployeeID
            WHERE YEAR(a.AttendanceMonth) = :year {month_filter}
            GROUP BY e.EmployeeID, e.FullName
            ORDER BY WorkDays DESC LIMIT 5
        """
        return self.execute_query(sql, params={"month": month, "year": year}, fetch=True)

    def get_top_absent_employees(self, month=None, year=2026):
        """Top 5 nhân viên nghỉ nhiều nhất (Cộng dồn nếu lọc theo năm)"""
        month_filter = "AND MONTH(a.AttendanceMonth) = :month" if month else ""
        sql = f"""
            SELECT e.FullName, SUM(a.AbsentDays + a.LeaveDays) as TotalOff
            FROM attendance a
            JOIN employees_payroll e ON a.EmployeeID = e.EmployeeID
            WHERE YEAR(a.AttendanceMonth) = :year {month_filter}
            GROUP BY e.EmployeeID, e.FullName
            ORDER BY TotalOff DESC LIMIT 5
        """
        return self.execute_query(sql, params={"month": month, "year": year}, fetch=True)

    # --- CẢNH BÁO HỆ THỐNG (ALERTS) ---

    def get_alert_absenteeism(self, month, year):
        """Cảnh báo nghỉ > 3 ngày trong tháng"""
        sql = """
            SELECT e.FullName, d.DepartmentName, (a.AbsentDays + a.LeaveDays) as TotalOff
            FROM attendance a
            JOIN employees_payroll e ON a.EmployeeID = e.EmployeeID
            JOIN departments_payroll d ON e.DepartmentID = d.DepartmentID
            WHERE MONTH(a.AttendanceMonth) = :month AND YEAR(a.AttendanceMonth) = :year
              AND (a.AbsentDays + a.LeaveDays) > 3
        """
        return self.execute_query(sql, params={"month": month, "year": year}, fetch=True)

    def get_alert_unusual_salary(self, month, year):
        """Cảnh báo lương bất thường: Khấu trừ > 20% hoặc Net > 50tr"""
        sql = """
            SELECT e.FullName, s.NetSalary, s.Deductions, s.BaseSalary
            FROM salaries s
            JOIN employees_payroll e ON s.EmployeeID = e.EmployeeID
            WHERE MONTH(s.SalaryMonth) = :month AND YEAR(s.SalaryMonth) = :year
              AND (s.Deductions > (s.BaseSalary * 0.2) OR s.NetSalary > 50000000)
        """
        return self.execute_query(sql, params={"month": month, "year": year}, fetch=True)

    def get_alert_missing_attendance(self, month, year):
        """Cảnh báo nhân viên 'Đang làm việc' nhưng chưa có dữ liệu chấm công"""
        sql = """
            SELECT e.FullName, d.DepartmentName
            FROM employees_payroll e
            JOIN departments_payroll d ON e.DepartmentID = d.DepartmentID
            WHERE e.Status = 'Đang làm việc'
              AND e.EmployeeID NOT IN (
                SELECT DISTINCT EmployeeID FROM attendance 
                WHERE MONTH(AttendanceMonth) = :month AND YEAR(AttendanceMonth) = :year
                  AND EmployeeID IS NOT NULL
              )
        """
        return self.execute_query(sql, params={"month": month, "year": year}, fetch=True)