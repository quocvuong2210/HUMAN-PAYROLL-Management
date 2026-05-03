from flask import Blueprint
from src.controllers.attendenceController import AttendanceController

# Khởi tạo Blueprint cho Attendance
attendance_bp = Blueprint("attendance", __name__)
controller = AttendanceController()

# --- 1. NHÓM ROUTE CHẤM CÔNG ---

@attendance_bp.route("/", methods=["GET"])
def get_attendance():
    """
    Lấy danh sách chấm công theo tháng và các bộ lọc.
    URL: GET /api/attendance?month=2026-05-01&name=An&dept_id=1
    """
    return controller.get_attendance()

@attendance_bp.route("/", methods=["POST"])
def add_attendance():
    """
    Ghi nhận chấm công mới cho nhân viên.
    Body JSON: {"EmployeeID": 1, "WorkDays": 22, "AbsentDays": 1, "LeaveDays": 0}
    """
    return controller.add_attendance()

@attendance_bp.route("/<int:id>", methods=["PUT"])
def update_attendance(id):
    """
    Cập nhật dữ liệu chấm công hiện có.
    URL: PUT /api/attendance/10
    """
    return controller.update_attendance(id)

# --- 2. NHÓM ROUTE BÁO CÁO NHÂN SỰ ---

@attendance_bp.route("/missing", methods=["GET"])
def get_missing_attendance():
    """
    Lấy danh sách nhân viên chưa chấm công trong tháng hiện tại.
    URL: GET /api/attendance/missing?dept_id=1
    """
    return controller.get_missing_attendance()