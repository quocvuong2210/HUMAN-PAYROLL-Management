from flask import Blueprint
from src.controllers.reportController import ReportController

report_bp = Blueprint("report", __name__)
controller = ReportController()

# =========================================
# 1. DASHBOARD (FULL)
# =========================================
@report_bp.route("/dashboard", methods=["GET"])
def get_dashboard():
    return controller.get_dashboard()


# =========================================
# 2. SALARY BY DEPARTMENT
# =========================================
@report_bp.route("/salary-by-department", methods=["GET"])
def salary_by_department():
    return controller.get_salary_by_department()


# =========================================
# 3. EMPLOYEE DISTRIBUTION
# =========================================
@report_bp.route("/employee-distribution", methods=["GET"])
def employee_distribution():
    return controller.get_employee_distribution()


# =========================================
# 4. POSITION REPORT
# =========================================
@report_bp.route("/position", methods=["GET"])
def position_report():
    return controller.get_position_report()


# =========================================
# 5. ATTENDANCE REPORT
# =========================================
@report_bp.route("/attendance", methods=["GET"])
def attendance_report():
    return controller.get_attendance_report()


# =========================================
# 6. PAYROLL DETAIL
# =========================================
@report_bp.route("/payroll", methods=["GET"])
def payroll_detail():
    return controller.get_payroll_detail()


# =========================================
# 7. ALERT REPORT
# =========================================
@report_bp.route("/alert", methods=["GET"])
def alert_report():
    return controller.get_alert_report()


# =========================================
# 8. TOP DEPARTMENT (TỐN NHẤT)
# =========================================
@report_bp.route("/top-department", methods=["GET"])
def top_department():
    return controller.get_top_department()


# =========================================
# 9. BEST EMPLOYEE
# =========================================
@report_bp.route("/best-employee", methods=["GET"])
def best_employee():
    return controller.get_best_employee()