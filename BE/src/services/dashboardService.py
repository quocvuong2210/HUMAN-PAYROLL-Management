from src.models.dashboardModel import DashboardModel

class DashboardService:
    def __init__(self):
        # Khởi tạo 2 kết nối riêng biệt
        self.db_mysql = DashboardModel(db_type="mysql") 
        self.db_mssql = DashboardModel(db_type="mssql") 

    # --- CÁC HÀM CŨ CỦA BẠN ---
    

    

    def get_all_employees(self):
        return self.db_mssql.get_total_employees()

    def get_employee_by_id(self, emp_id):
        return self.db_mssql.get_employee_by_id(emp_id)

    # --- HÀM THỐNG KÊ TỔNG HỢP MỚI ---
    def get_dashboard_summary(self):
        """
        Tổng hợp dữ liệu từ cả 2 database để hiển thị lên Dashboard
        """
        # 1. Lấy dữ liệu nhân sự từ SQL Server
        total_employees = self.db_mssql.get_total_employees()
        print(f"Total Employees (MSSQL): {total_employees}")
        total_departments = self.db_mssql.get_total_departments()

        # 2. Lấy dữ liệu tài chính từ MySQL
        payroll_stats = self.db_mysql.get_payroll_stats()

        # 3. Đóng gói kết quả trả về cho Controller
        return {
           
            "total_employees": total_employees,
            "total_departments": total_departments,
            "total_net_salary": payroll_stats['TotalNetSalary'] if payroll_stats else 0,
            "total_bonus": payroll_stats['TotalBonus'] if payroll_stats else 0,
            "total_deductions": payroll_stats['TotalDeductions'] if payroll_stats else 0,
           
        }
    def get_chart_data(self, month=None, year=2026):
        return {
            "salary_by_dept": self.db_mysql.get_salary_by_department(month, year),
            "salary_trend": self.db_mysql.get_salary_trend(year),
            "status_distribution": self.db_mysql.get_employee_status_distribution()
        }
    def get_attendance_report(self, month, year):
        return {
            "avg_workdays": self.db_mysql.get_avg_workdays(month, year),
            "top_diligent": self.db_mysql.get_top_diligent_employees(month, year),
            "top_absent": self.db_mysql.get_top_absent_employees(month, year)
        }
    def get_system_alerts(self, month, year):
        return {
            "high_absence": self.db_mysql.get_alert_absenteeism(month, year),
            "unusual_salary": self.db_mysql.get_alert_unusual_salary(month, year),
            "missing_data": self.db_mysql.get_alert_missing_attendance(month, year)
        }
    # Lấy lẻ Sinh nhật
    def get_only_birthdays(self, month):
        return self.mssql_model.get_birthdays(month)

    # Lấy lẻ Kỷ niệm
    def get_only_anniversaries(self, month):
        return self.mssql_model.get_work_anniversaries(month)

    # Lấy lẻ Nghỉ quá buổi
    def get_only_high_absence(self, month, year):
        return self.mysql_model.get_high_absenteeism(month, year)

    # Lấy lẻ Lương bất thường
    def get_only_unusual_salaries(self, month, year):
        return self.mysql_model.get_unusual_salaries(month, year)