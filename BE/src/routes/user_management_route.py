"""
User Management Routes - API endpoints cho quản lý user
"""
from flask import Blueprint
from src.controllers.user_management_controller import UserManagementController
from src.middleware.rbac_middleware import token_required, require_permission

# Tạo Blueprint
user_management_bp = Blueprint('user_management', __name__)

# Khởi tạo controller
controller = UserManagementController()

# ==================== USER CRUD ====================

@user_management_bp.route('/create', methods=['POST'])
@token_required
@require_permission("USER_CREATE")
def create_user(**kwargs):
    """Tạo user mới với roles"""
    return controller.create_user(**kwargs)

@user_management_bp.route('', methods=['GET'])
@token_required
@require_permission("USER_VIEW")
def get_all_users(**kwargs):
    """Lấy danh sách tất cả users"""
    return controller.get_all_users(**kwargs)

@user_management_bp.route('/<int:user_id>', methods=['GET'])
@token_required
@require_permission("USER_VIEW")
def get_user_by_id(user_id, **kwargs):
    """Lấy thông tin chi tiết user"""
    return controller.get_user_by_id(user_id, **kwargs)

@user_management_bp.route('/<int:user_id>', methods=['PUT'])
@token_required
@require_permission("USER_EDIT")
def update_user(user_id, **kwargs):
    """Cập nhật thông tin user"""
    return controller.update_user(user_id, **kwargs)

@user_management_bp.route('/<int:user_id>', methods=['DELETE'])
@token_required
@require_permission("USER_DELETE")
def delete_user(user_id, **kwargs):
    """Xóa user"""
    return controller.delete_user(user_id, **kwargs)

# ==================== USER ROLES ====================

@user_management_bp.route('/<int:user_id>/roles', methods=['PUT'])
@token_required
@require_permission("USER_EDIT")
def update_user_roles(user_id, **kwargs):
    """Cập nhật roles của user"""
    return controller.update_user_roles(user_id, **kwargs)

@user_management_bp.route('/<int:user_id>/roles', methods=['POST'])
@token_required
@require_permission("USER_EDIT")
def add_role_to_user(user_id, **kwargs):
    """Thêm role cho user"""
    return controller.add_role_to_user(user_id, **kwargs)

@user_management_bp.route('/<int:user_id>/roles/<int:role_id>', methods=['DELETE'])
@token_required
@require_permission("USER_EDIT")
def remove_role_from_user(user_id, role_id, **kwargs):
    """Xóa role khỏi user"""
    return controller.remove_role_from_user(user_id, role_id, **kwargs)
