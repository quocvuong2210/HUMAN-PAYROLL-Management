"""
User Route V2 - Production-Ready User Management with RBAC
Routes for user creation with roles, email verification
"""
from flask import Blueprint
from src.controllers.user_controller_v2 import UserControllerV2

# Create blueprint
user_v2_bp = Blueprint('user_v2', __name__)

# Initialize controller
user_controller = UserControllerV2()

# ==================== USER CREATION WITH ROLES ====================

@user_v2_bp.route('/users', methods=['POST'])
def create_user_with_roles():
    """
    POST /api/v1/auth/users
    Tạo user mới với roles
    
    Body:
    {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "password123",
        "phoneNumber": "0123456789",
        "dateOfBirth": "1990-01-01",
        "gender": "Nam",
        "roleIds": [1, 2]
    }
    """
    return user_controller.create_user_with_roles()

# ==================== ROLE MANAGEMENT ====================

@user_v2_bp.route('/roles', methods=['GET'])
def get_all_roles():
    """
    GET /api/v1/auth/roles
    Lấy danh sách tất cả roles
    """
    return user_controller.get_all_roles()

# ==================== EMAIL VERIFICATION ====================

@user_v2_bp.route('/verify-email', methods=['GET'])
def verify_email():
    """
    GET /api/v1/auth/verify-email?token=abc123
    Xác nhận email bằng token
    """
    return user_controller.verify_email()

@user_v2_bp.route('/resend-verification', methods=['POST'])
def resend_verification_email():
    """
    POST /api/v1/auth/resend-verification
    Gửi lại email xác nhận
    
    Body:
    {
        "email": "john@example.com"
    }
    """
    return user_controller.resend_verification_email()
