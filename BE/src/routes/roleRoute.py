"""
Role Routes - API endpoints cho quản lý vai trò
"""
from flask import Blueprint
from src.controllers.role_controller import RoleController

# Tạo Blueprint
role_bp = Blueprint('role', __name__)

# Khởi tạo controller
controller = RoleController()

@role_bp.route('/roles', methods=['GET'])
def get_all_roles():
    """Lấy danh sách tất cả roles"""
    return controller.get_all_roles()

@role_bp.route('/users/<int:user_id>/roles', methods=['GET'])
def get_user_roles(user_id):
    """Lấy danh sách roles của user"""
    return controller.get_user_roles(user_id)

@role_bp.route('/users/<int:user_id>/roles', methods=['PUT'])
def update_user_roles(user_id):
    """Cập nhật roles của user"""
    return controller.update_user_roles(user_id)

@role_bp.route('/roles/<int:role_id>/permissions', methods=['GET'])
def get_role_permissions(role_id):
    """Lấy danh sách permissions của role"""
    return controller.get_role_permissions(role_id)
