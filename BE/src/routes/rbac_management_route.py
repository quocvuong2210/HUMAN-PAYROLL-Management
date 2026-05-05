"""
RBAC Management Routes - API endpoints cho quản lý RBAC
"""
from flask import Blueprint
from src.controllers.rbac_management_controller import RBACManagementController
from src.middleware.rbac_middleware import token_required, require_role

# Tạo Blueprint
rbac_management_bp = Blueprint('rbac_management', __name__)

# Khởi tạo controller
controller = RBACManagementController()

# ==================== ROLE PERMISSIONS ====================

@rbac_management_bp.route('/roles/<int:role_id>/permissions', methods=['GET'])
@token_required
def get_role_permissions(role_id, **kwargs):
    """Lấy danh sách permissions của role"""
    return controller.get_role_permissions(role_id, **kwargs)

@rbac_management_bp.route('/roles/<int:role_id>/permissions', methods=['PUT'])
@token_required
@require_role("ADMIN")
def update_role_permissions(role_id, **kwargs):
    """Cập nhật permissions của role (Chỉ ADMIN)"""
    return controller.update_role_permissions(role_id, **kwargs)

@rbac_management_bp.route('/roles/<int:role_id>/permissions', methods=['POST'])
@token_required
@require_role("ADMIN")
def add_permission_to_role(role_id, **kwargs):
    """Thêm permission cho role (Chỉ ADMIN)"""
    return controller.add_permission_to_role(role_id, **kwargs)

@rbac_management_bp.route('/roles/<int:role_id>/permissions/<int:permission_id>', methods=['DELETE'])
@token_required
@require_role("ADMIN")
def remove_permission_from_role(role_id, permission_id, **kwargs):
    """Xóa permission khỏi role (Chỉ ADMIN)"""
    return controller.remove_permission_from_role(role_id, permission_id, **kwargs)

# ==================== PERMISSION FUNCTIONS ====================

@rbac_management_bp.route('/permissions/<int:permission_id>/functions', methods=['GET'])
@token_required
def get_permission_functions(permission_id, **kwargs):
    """Lấy danh sách functions của permission"""
    return controller.get_permission_functions(permission_id, **kwargs)

# ==================== ROLE MANAGEMENT ====================

@rbac_management_bp.route('/roles', methods=['POST'])
@token_required
@require_role("ADMIN")
def create_role(**kwargs):
    """Tạo role mới (Chỉ ADMIN)"""
    return controller.create_role(**kwargs)

@rbac_management_bp.route('/roles/<int:role_id>', methods=['PUT'])
@token_required
@require_role("ADMIN")
def update_role(role_id, **kwargs):
    """Cập nhật thông tin role (Chỉ ADMIN)"""
    return controller.update_role(role_id, **kwargs)

@rbac_management_bp.route('/roles/<int:role_id>', methods=['DELETE'])
@token_required
@require_role("ADMIN")
def delete_role(role_id, **kwargs):
    """Xóa role (Chỉ ADMIN)"""
    return controller.delete_role(role_id, **kwargs)

# ==================== STATISTICS ====================

@rbac_management_bp.route('/statistics', methods=['GET'])
@token_required
def get_statistics(**kwargs):
    """Lấy thống kê RBAC"""
    return controller.get_rbac_statistics(**kwargs)
