"""
User Admin Routes - Routes cho admin quản lý users
"""
from flask import Blueprint
from src.controllers.user_admin_controller import UserAdminController

user_admin_bp = Blueprint('user_admin', __name__)
controller = UserAdminController()

@user_admin_bp.route('/users-with-roles', methods=['GET'])
def get_all_users_with_roles():
    """
    GET /api/v1/admin/users-with-roles
    Lấy tất cả users kèm roles
    
    Requires: SUPER_ADMIN or HR_MANAGER role
    """
    return controller.get_all_users_with_roles()

@user_admin_bp.route('/access-logs', methods=['GET'])
def get_all_access_logs():
    """
    GET /api/v1/admin/access-logs
    Lấy tất cả lịch sử truy cập
    
    Requires: SUPER_ADMIN or HR_MANAGER role
    """
    return controller.get_all_access_logs()
