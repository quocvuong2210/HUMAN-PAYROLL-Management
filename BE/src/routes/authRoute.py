from flask import Blueprint, request, jsonify
from src.controllers.authController import AuthController

# Khởi tạo Blueprint
auth_bp = Blueprint('auth', __name__)
# Khởi tạo Controller
auth_controller = AuthController()

# --- 1. AUTHENTICATION ROUTES ---
@auth_bp.route('/register', methods=['POST'])
def register():
    return auth_controller.register()

@auth_bp.route('/login', methods=['POST'])
def login():
    return auth_controller.login()

# --- 2. PROFILE ROUTE ---
@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    return auth_controller.get_profile()
@auth_bp.route('/user-info/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    return auth_controller.get_user_info(user_id)
@auth_bp.route('/admin/users', methods=['GET'])
def get_users():
    return auth_controller.get_all_users_list()

@auth_bp.route('/admin/logs', methods=['GET'])
def get_logs():
    return auth_controller.get_full_system_logs()
# --- 3. QUẢN TRỊ USER (CRUD) ---

@auth_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Cập nhật thông tin user"""
    return auth_controller.update_user(user_id)

@auth_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Xóa user (Dữ liệu log/role liên quan sẽ bị xóa theo)"""
    return auth_controller.delete_user(user_id)
@auth_bp.route('/change-password', methods=['PUT'])
def change_password():
    """Route đổi mật khẩu cho người dùng hiện tại"""
    return auth_controller.change_password() 