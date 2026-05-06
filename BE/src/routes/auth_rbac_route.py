"""
Auth RBAC Routes - Routes cho authentication với RBAC
"""
from flask import Blueprint
from src.controllers.auth_rbac_controller import AuthRBACController

# Tạo blueprint
auth_rbac_bp = Blueprint('auth_rbac', __name__, url_prefix='/api/v1/auth')

# Khởi tạo controller
controller = AuthRBACController()

# ==================== PUBLIC ROUTES ====================

# Đăng ký
auth_rbac_bp.route('/register', methods=['POST'])(controller.register)

# Đăng nhập
auth_rbac_bp.route('/login', methods=['POST'])(controller.login)

# Refresh token
auth_rbac_bp.route('/refresh-token', methods=['POST'])(controller.refresh_token)

# ==================== PROTECTED ROUTES ====================

# Logout (yêu cầu token)
auth_rbac_bp.route('/logout', methods=['POST'])(controller.logout)

# Get current user info
auth_rbac_bp.route('/me', methods=['GET'])(controller.get_me)

# Change password
auth_rbac_bp.route('/change-password', methods=['POST'])(controller.change_password)

# Update profile
auth_rbac_bp.route('/profile', methods=['PUT'])(controller.update_profile)

# Get my access logs
auth_rbac_bp.route('/my-access-logs', methods=['GET'])(controller.get_my_access_logs)

# ==================== ADMIN ROUTES (SUPER_ADMIN ONLY) ====================

# Get all roles (yêu cầu đăng nhập)
auth_rbac_bp.route('/roles', methods=['GET'])(controller.get_all_roles)

# Create user with roles
auth_rbac_bp.route('/users', methods=['POST'])(controller.create_user_with_roles)

# Update user
auth_rbac_bp.route('/users/<int:user_id>', methods=['PUT'])(controller.update_user)

# Delete user
auth_rbac_bp.route('/users/<int:user_id>', methods=['DELETE'])(controller.delete_user)
