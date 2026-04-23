from flask import Blueprint
from src.controllers.dashboardController import DashboardController


dashboard_bp = Blueprint("dashboard", __name__)
controller = DashboardController()


@dashboard_bp.route("/salaries", methods=["GET"])
def get_all_salaries():
    return controller.get_all_salaries()
@dashboard_bp.route("/salaries/<int:id>", methods=["GET"])

@dashboard_bp.route("/employees", methods=["GET"])
def get_all_employees():
    return controller.get_all_employees()

@dashboard_bp.route("/summary", methods=["GET"])
def get_dashboard_summary():
    """
    Endpoint: /summary?month=9&year=2024
    Trả về: Tổng nhân viên, phòng ban, lương, thưởng, khấu trừ.
    """
    return controller.get_dashboard_summary()
@dashboard_bp.route("/charts", methods=["GET"])
def get_dashboard_charts():
    """
    Dùng cho 3 biểu đồ (Bar, Line, Pie)
    Endpoint: /charts?month=9&year=2024
    - month: (Tùy chọn) lọc biểu đồ cột theo tháng
    - year: (Mặc định năm hiện tại) lọc dữ liệu theo năm
    """
    return controller.get_charts()
@dashboard_bp.route("/attendance", methods=["GET"])
def get_attendance_stats():
    return controller.get_attendance_stats()
@dashboard_bp.route("/alerts", methods=["GET"])
def get_alerts():
    return controller.get_alerts()