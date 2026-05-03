from flask import Blueprint
from src.controllers.salaryController import SalaryController

# Khởi tạo Blueprint cho Salary
salary_bp = Blueprint("salary", __name__)
controller = SalaryController()

# --- 1. NHÓM ROUTE QUẢN LÝ LƯƠNG ---

@salary_bp.route("/", methods=["GET"])
def get_salaries():
    """
    Lấy danh sách lương theo tháng và các bộ lọc (phòng ban, vị trí, trạng thái).
    URL: GET /api/salary?month=2026-05-01&status=pending&dept_id=1
    """
    return controller.get_salary_list()

@salary_bp.route("/process", methods=["POST"])
def process_salary():
    """
    Tính và lưu lương cho nhân viên.
    Body JSON: {"EmployeeID": 1, "SalaryMonth": "2026-05-01", "BaseSalary": 10000000, "Bonus": 500000, "Deductions": 0}
    """
    return controller.process_salary()

@salary_bp.route("/<int:id>", methods=["PUT"])
def update_salary(id):
    """
    Cập nhật dữ liệu lương đã tính.
    URL: PUT /api/salary/10
    """
    return controller.update_salary(id)

# --- 2. NHÓM ROUTE LỊCH SỬ LƯƠNG ---

@salary_bp.route("/history/<int:employee_id>", methods=["GET"])
def get_salary_history(employee_id):
    """
    Lấy lịch sử lương của một nhân viên cụ thể.
    URL: GET /api/salary/history/5
    """
    return controller.get_salary_history(employee_id)
# --- 3. NHÓM ROUTE XUẤT BÁO CÁO ---

@salary_bp.route("/export", methods=["GET"])
def export_salary():
    """
    Xuất báo cáo lương ra file Excel.
    URL: GET /api/salary/export?month=2026-05
    """
    return controller.export_salary_report()