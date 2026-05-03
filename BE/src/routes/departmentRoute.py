from flask import Blueprint
from src.controllers.departmentController import DepartmentController

# Khởi tạo Blueprint cho Department
department_bp = Blueprint("department", __name__)
controller = DepartmentController()

# --- CÁC ROUTE TRUY XUẤT (READ) ---

@department_bp.route("/", methods=["GET"])
def get_departments():
    """
    Lấy danh sách tất cả phòng ban + Thống kê (Số NV, Tổng lương)
    Hỗ trợ: ?search=...&sort=...&order=...
    """
    return controller.get_all_departments()

@department_bp.route("/<int:dept_id>", methods=["GET"])
def get_department_detail(dept_id):
    """Lấy chi tiết một phòng ban"""
    return controller.get_department_by_id(dept_id)

@department_bp.route("/stats", methods=["GET"])
def get_department_stats():
    """
    Endpoint riêng nếu muốn lấy chỉ dữ liệu thống kê biểu đồ
    """
    return controller.get_department_stats()


# --- CÁC ROUTE THAO TÁC DỮ LIỆU (CUD) ---

@department_bp.route("/", methods=["POST"])
def create_department():
    """Tạo mới phòng ban (Đồng bộ MSSQL -> MySQL)"""
    return controller.create_department()

@department_bp.route("/<int:dept_id>", methods=["PUT"])
def update_department(dept_id):
    """Cập nhật phòng ban"""
    return controller.update_department(dept_id)

@department_bp.route("/<int:dept_id>", methods=["DELETE"])
def delete_department(dept_id):
    """Xóa phòng ban"""
    return controller.delete_department(dept_id)


# --- ROUTE HỆ THỐNG (SYSTEM) ---

@department_bp.route("/sync", methods=["POST"])
def sync_departments():
    """
    Endpoint: POST /api/v1/departments/sync
    Ép buộc đồng bộ dữ liệu từ MSSQL sang MySQL
    """
    return controller.sync_data()