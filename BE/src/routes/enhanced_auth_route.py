"""
Enhanced Auth Routes - Định nghĩa các API endpoints với RBAC
"""
from flask import Blueprint
from src.controllers.enhanced_auth_controller import EnhancedAuthController
from src.middleware.rbac_middleware import (
    token_required,
    require_permission,
    require_role,
    optional_auth
)

# Tạo Blueprint
enhanced_auth_bp = Blueprint('enhanced_auth', __name__)

# Khởi tạo controller
controller = EnhancedAuthController()

# ==================== PUBLIC ROUTES (Không cần token) ====================

@enhanced_auth_bp.route('/register', methods=['POST'])
def register():
    """Đăng ký user mới"""
    return controller.register()

@enhanced_auth_bp.route('/verify-email', methods=['GET'])
def verify_email():
    """Xác nhận email"""
    return controller.verify_email()

@enhanced_auth_bp.route('/resend-verification', methods=['POST'])
def resend_verification():
    """Gửi lại email xác nhận"""
    return controller.resend_verification()

@enhanced_auth_bp.route('/login', methods=['POST'])
def login():
    """Đăng nhập"""
    return controller.login()

@enhanced_auth_bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    """Làm mới access token"""
    return controller.refresh_token()

@enhanced_auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Yêu cầu reset password"""
    return controller.forgot_password()

@enhanced_auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Đặt lại mật khẩu"""
    return controller.reset_password()

# ==================== PROTECTED ROUTES (Cần token) ====================

@enhanced_auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(**kwargs):
    """Đăng xuất"""
    return controller.logout()

# ==================== USER ROUTES ====================

@enhanced_auth_bp.route('/me', methods=['GET'])
@token_required
def get_profile(**kwargs):
    """Lấy thông tin profile của user hiện tại"""
    return controller.get_profile(**kwargs)

@enhanced_auth_bp.route('/me/permissions', methods=['GET'])
@token_required
def get_my_permissions(**kwargs):
    """Lấy danh sách quyền của user hiện tại"""
    return controller.get_my_permissions(**kwargs)

# ==================== ADMIN ROUTES - USER MANAGEMENT ====================

@enhanced_auth_bp.route('/admin/users/assign-role', methods=['POST'])
@token_required
@require_permission("USER_EDIT")
def assign_role(**kwargs):
    """Gán role cho user (Cần quyền USER_EDIT)"""
    return controller.assign_role(**kwargs)

@enhanced_auth_bp.route('/admin/users/remove-role', methods=['POST'])
@token_required
@require_permission("USER_EDIT")
def remove_role(**kwargs):
    """Xóa role khỏi user (Cần quyền USER_EDIT)"""
    return controller.remove_role(**kwargs)

@enhanced_auth_bp.route('/admin/users/<int:user_id>/roles', methods=['GET'])
@token_required
@require_permission("USER_VIEW")
def get_user_roles(user_id, **kwargs):
    """Lấy danh sách role của user (Cần quyền USER_VIEW)"""
    return controller.get_user_roles(user_id)

# ==================== ADMIN ROUTES - RBAC MANAGEMENT ====================

@enhanced_auth_bp.route('/admin/roles', methods=['GET'])
@token_required
@require_role("ADMIN", "HR_MANAGER")
def get_all_roles(**kwargs):
    """Lấy danh sách tất cả roles (Cần role ADMIN hoặc HR_MANAGER)"""
    return controller.get_all_roles(**kwargs)

@enhanced_auth_bp.route('/admin/permissions', methods=['GET'])
@token_required
@require_role("ADMIN")
def get_all_permissions(**kwargs):
    """Lấy danh sách tất cả permissions (Chỉ ADMIN)"""
    return controller.get_all_permissions(**kwargs)

@enhanced_auth_bp.route('/admin/functions', methods=['GET'])
@token_required
@require_role("ADMIN")
def get_all_functions(**kwargs):
    """Lấy danh sách tất cả system functions (Chỉ ADMIN)"""
    return controller.get_all_functions(**kwargs)

# ==================== HEALTH CHECK ====================

@enhanced_auth_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {
        "status": "success",
        "message": "Enhanced Auth API is running",
        "version": "1.0.0"
    }, 200
