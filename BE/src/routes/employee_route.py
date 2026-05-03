from flask import Blueprint
from src.controllers.employee_controller import EmployeeController

# Khởi tạo Blueprint cho Employee
employee_bp = Blueprint("employee", __name__)
controller = EmployeeController()

# --- 1. NHÓM ROUTE TIỆN ÍCH (METADATA) ---

@employee_bp.route("/metadata", methods=["GET"])
def get_metadata():
    """
    Lấy danh sách Departments, Positions, Statuses, Genders.
    Dùng để đổ dữ liệu vào các thanh lọc (Filter bar) và Form thêm/sửa.
    URL: GET /api/employees/metadata
    """
    return controller.get_metadata()


# --- 2. NHÓM ROUTE ĐỌC DỮ LIỆU (READ) ---

@employee_bp.route("/", methods=["GET"])
def get_employees():
    """
    Lấy danh sách nhân viên với bộ lọc đầy đủ và phân trang.
    Các tham số hỗ trợ (Query Params):
    - Tìm kiếm: name, status, gender, dept_id, pos_id
    - Khoảng ngày: start_date, end_date (YYYY-MM-DD)
    - Phân trang: page, limit
    URL ví dụ: GET /api/employees?page=1&limit=10&dept_id=2&gender=Nam
    """
    return controller.get_employees()

@employee_bp.route("/<int:id>", methods=["GET"])
def get_employee_detail(id):
    """
    Lấy chi tiết profile (MSSQL) + Lịch sử lương & Chuyên cần (MySQL).
    URL: GET /api/employees/101
    """
    return controller.get_employee_detail(id)


# --- 3. NHÓM ROUTE THAY ĐỔI DỮ LIỆU (CUD) ---

@employee_bp.route("/", methods=["POST"])
def add_employee():
    """
    Thêm mới nhân viên: Lưu MSSQL và tự động Sync MySQL.
    Body JSON yêu cầu các trường: FullName, Email, PhoneNumber, HireDate, DepartmentID, PositionID, Gender...
    """
    return controller.add_employee()

@employee_bp.route("/<int:id>", methods=["PUT"])
def update_employee(id):
    """
    Cập nhật thông tin nhân viên và đồng bộ lại 2 DB.
    URL: PUT /api/employees/101
    """
    return controller.update_employee(id)

@employee_bp.route("/<int:id>", methods=["DELETE"])
def delete_employee(id):
    """
    Xóa sạch dữ liệu liên quan trên cả 2 database.
    Thao tác này sẽ xóa: salaries, attendance, employees_payroll (MySQL) và Employees (MSSQL).
    URL: DELETE /api/employees/101
    """
    return controller.delete_employee(id)
# --- 4. NHÓM ROUTE ĐỒNG BỘ (SYNC) ---

@employee_bp.route("/sync", methods=["POST"])
def sync_all_employees():
    """
    Kích hoạt tiến trình quét và đồng bộ toàn bộ nhân viên từ MSSQL sang MySQL.
    Sử dụng khi cần cập nhật lại toàn bộ danh sách hoặc bù đắp dữ liệu thiếu.
    URL: POST /api/employees/sync
    """
    return controller.sync_all()