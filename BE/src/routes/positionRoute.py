from flask import Blueprint
from src.controllers.positionController import PositionController

# Khởi tạo Blueprint cho Position
# Chú ý: Nên đăng ký prefix "/api/v1/positions" trong app.py để đồng bộ với Frontend
position_bp = Blueprint("position", __name__)
controller = PositionController()

# --- CÁC ROUTE TRUY XUẤT (READ) ---
# Ưu tiên lấy từ MySQL (Slave) để giảm tải cho Master

@position_bp.route("/", methods=["GET"])
def get_positions():
    """
    Endpoint: GET /api/v1/positions?search=...
    Lấy danh sách chức vụ kèm thống kê TotalEmployees từ MySQL.
    """
    return controller.get_all_positions()

@position_bp.route("/<int:pos_id>", methods=["GET"])
def get_position_detail(pos_id):
    """
    Endpoint: GET /api/v1/positions/1
    Lấy chi tiết 1 chức vụ từ hệ thống.
    """
    return controller.get_position_by_id(pos_id)

# --- CÁC ROUTE THAO TÁC DỮ LIỆU ĐỒNG BỘ (CUD) ---
# Các thao tác Ghi (Ghi vào MSSQL Master trước -> Đồng bộ sang MySQL Slave)

@position_bp.route("/", methods=["POST"])
def create_position():
    """
    Endpoint: POST /api/v1/positions
    Body: { "PositionName": "Kỹ sư" }
    Quy trình: Kiểm tra trùng -> MSSQL tạo ID -> MySQL đồng bộ.
    """
    return controller.create_position()

@position_bp.route("/<int:pos_id>", methods=["PUT"])
def update_position(pos_id):
    """
    Endpoint: PUT /api/v1/positions/1
    Body: { "PositionName": "Kỹ sư cấp cao" }
    Cập nhật đồng bộ tên chức vụ trên cả 2 Database.
    """
    return controller.update_position(pos_id)

@position_bp.route("/<int:pos_id>", methods=["DELETE"])
def delete_position(pos_id):
    """
    Endpoint: DELETE /api/v1/positions/1
    Ràng buộc: Controller/Service sẽ kiểm tra bảng employees_payroll (MySQL) 
    để chắc chắn chức vụ không còn nhân viên nào trước khi cho phép xóa ở Master.
    """
    return controller.delete_position(pos_id)

# --- ROUTE HỆ THỐNG (SYSTEM) ---

@position_bp.route("/sync", methods=["POST"])
def force_sync():
    """
    Endpoint: POST /api/v1/positions/sync
    Dùng khi dữ liệu MySQL bị lệch so với MSSQL (Master).
    Thực hiện ghi đè dữ liệu từ Master sang Slave.
    """
    return controller.sync_all_positions()