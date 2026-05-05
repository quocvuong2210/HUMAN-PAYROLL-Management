"""
Auth RBAC Controller - Đăng nhập/Đăng ký với RBAC integration
"""
from flask import jsonify, request
from src.services.auth_rbac_service import AuthRBACService
from src.utils.jwt_rbac_helper import jwt_required, roles_required

class AuthRBACController:
    def __init__(self):
        self.auth_service = AuthRBACService()
    
    # ==================== ĐĂNG KÝ ====================
    
    def register(self):
        """
        POST /api/v1/auth/register
        Đăng ký user mới
        
        Body:
            - username (required): Tên đăng nhập
            - email (required): Email
            - password (required): Mật khẩu (tối thiểu 6 ký tự)
            - phone (optional): Số điện thoại
            - dob (optional): Ngày sinh (YYYY-MM-DD)
            - gender (optional): Giới tính (Nam/Nữ)
        
        Response:
            201: Đăng ký thành công
            400: Lỗi validation hoặc username/email đã tồn tại
            500: Lỗi server
        """
        try:
            data = request.get_json()
            
            # Validate required fields
            required = ['username', 'email', 'password']
            if not data or not all(k in data for k in required):
                return jsonify({
                    "status": "error",
                    "message": "Thiếu thông tin bắt buộc (username, email, password)"
                }), 400
            
            # Validate password length
            if len(data.get('password', '')) < 6:
                return jsonify({
                    "status": "error",
                    "message": "Mật khẩu phải có ít nhất 6 ký tự"
                }), 400
            
            # Call service
            result = self.auth_service.register(data)
            
            status_code = 201 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== ĐĂNG NHẬP ====================
    
    def login(self):
        """
        POST /api/v1/auth/login
        Đăng nhập và nhận JWT token với roles
        
        Body:
            - username (required): Tên đăng nhập
            - password (required): Mật khẩu
        
        Response:
            200: Đăng nhập thành công, trả về token và user info
            400: Thiếu thông tin
            401: Sai username/password hoặc tài khoản bị khóa
            500: Lỗi server
        """
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return jsonify({
                    "status": "error",
                    "message": "Thiếu username hoặc password"
                }), 400
            
            # Call service với request object để lấy IP và User Agent
            result = self.auth_service.login(username, password, request)
            
            status_code = 200 if result["status"] == "success" else 401
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== REFRESH TOKEN ====================
    
    def refresh_token(self):
        """
        POST /api/v1/auth/refresh-token
        Làm mới access token bằng refresh token
        
        Body:
            - refreshToken (required): Refresh token
        
        Response:
            200: Token mới
            401: Refresh token không hợp lệ
            500: Lỗi server
        """
        try:
            data = request.get_json()
            refresh_token = data.get('refreshToken')
            
            if not refresh_token:
                return jsonify({
                    "status": "error",
                    "message": "Thiếu refresh token"
                }), 400
            
            result = self.auth_service.refresh_access_token(refresh_token)
            
            status_code = 200 if result["status"] == "success" else 401
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== LOGOUT ====================
    
    @jwt_required
    def logout(self, **kwargs):
        """
        POST /api/v1/auth/logout
        Đăng xuất (optional: thu hồi refresh token)
        
        Headers:
            - Authorization: Bearer <access_token>
        
        Body (optional):
            - refreshToken: Refresh token cần thu hồi
        
        Response:
            200: Đăng xuất thành công
            401: Token không hợp lệ
            500: Lỗi server
        """
        try:
            data = request.get_json() or {}
            refresh_token = data.get('refreshToken')
            
            result = self.auth_service.logout(refresh_token)
            
            return jsonify(result), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== GET CURRENT USER ====================
    
    @jwt_required
    def get_me(self, current_user_id, current_username, current_user_roles, **kwargs):
        """
        GET /api/v1/auth/me
        Lấy thông tin user hiện tại từ token
        
        Headers:
            - Authorization: Bearer <access_token>
        
        Response:
            200: Thông tin user
            401: Token không hợp lệ
            500: Lỗi server
        """
        try:
            result = self.auth_service.get_user_profile(current_user_id)
            
            status_code = 200 if result["status"] == "success" else 404
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== CHANGE PASSWORD ====================
    
    @jwt_required
    def change_password(self, current_user_id, **kwargs):
        """
        POST /api/v1/auth/change-password
        Đổi mật khẩu
        
        Headers:
            - Authorization: Bearer <access_token>
        
        Body:
            - oldPassword (required): Mật khẩu cũ
            - newPassword (required): Mật khẩu mới (tối thiểu 6 ký tự)
        
        Response:
            200: Đổi mật khẩu thành công
            400: Mật khẩu cũ không đúng hoặc validation lỗi
            401: Token không hợp lệ
            500: Lỗi server
        """
        try:
            data = request.get_json()
            old_password = data.get('oldPassword')
            new_password = data.get('newPassword')
            
            if not old_password or not new_password:
                return jsonify({
                    "status": "error",
                    "message": "Thiếu mật khẩu cũ hoặc mật khẩu mới"
                }), 400
            
            if len(new_password) < 6:
                return jsonify({
                    "status": "error",
                    "message": "Mật khẩu mới phải có ít nhất 6 ký tự"
                }), 400
            
            result = self.auth_service.change_password(current_user_id, old_password, new_password)
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== UPDATE PROFILE ====================
    
    @jwt_required
    def update_profile(self, current_user_id, **kwargs):
        """
        PUT /api/v1/auth/profile
        Cập nhật thông tin profile của user hiện tại
        
        Headers:
            - Authorization: Bearer <access_token>
        
        Body:
            - email (optional)
            - phone (optional)
            - dob (optional): YYYY-MM-DD
            - gender (optional): Nam/Nữ
        
        Response:
            200: Cập nhật thành công
            400: Lỗi validation
            401: Token không hợp lệ
            500: Lỗi server
        """
        try:
            data = request.get_json()
            result = self.auth_service.update_user_profile(current_user_id, data)
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== GET MY ACCESS LOGS ====================
    
    @jwt_required
    def get_my_access_logs(self, current_user_id, **kwargs):
        """
        GET /api/v1/auth/my-access-logs
        Lấy lịch sử truy cập của user hiện tại
        
        Headers:
            - Authorization: Bearer <access_token>
        
        Query params:
            - limit (optional): Số lượng logs (default: 50)
        
        Response:
            200: Danh sách access logs
            401: Token không hợp lệ
            500: Lỗi server
        """
        try:
            limit = request.args.get('limit', 50, type=int)
            result = self.auth_service.get_user_access_logs(current_user_id, limit)
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== CREATE USER WITH ROLES (SUPER_ADMIN ONLY) ====================
    
    @jwt_required
    @roles_required("SUPER_ADMIN")
    def create_user_with_roles(self, **kwargs):
        """
        POST /api/v1/auth/users
        Tạo user mới và gán roles (CHỈ SUPER_ADMIN)
        
        Headers:
            - Authorization: Bearer <access_token>
        
        Body:
            - username (required): Tên đăng nhập
            - email (required): Email
            - password (required): Mật khẩu
            - phone (optional): Số điện thoại
            - dob (optional): Ngày sinh
            - gender (optional): Giới tính
            - roleIds (optional): Array of role IDs [1, 2, 3]
        
        Response:
            201: Tạo user thành công
            400: Lỗi validation
            403: Không có quyền
            500: Lỗi server
        """
        try:
            data = request.get_json()
            
            # Validate required fields
            required = ['username', 'email', 'password']
            if not data or not all(k in data for k in required):
                return jsonify({
                    "status": "error",
                    "message": "Thiếu thông tin bắt buộc (username, email, password)"
                }), 400
            
            result = self.auth_service.create_user_with_roles(data)
            
            status_code = 201 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== UPDATE USER (SUPER_ADMIN ONLY) ====================
    
    @jwt_required
    @roles_required("SUPER_ADMIN")
    def update_user(self, user_id, **kwargs):
        """
        PUT /api/v1/auth/users/<user_id>
        Cập nhật thông tin user (CHỈ SUPER_ADMIN)
        
        Headers:
            - Authorization: Bearer <access_token>
        
        Body:
            - username (optional)
            - email (optional)
            - phone (optional)
            - dob (optional)
            - gender (optional)
            - status (optional): ACTIVE/INACTIVE
        
        Response:
            200: Cập nhật thành công
            400: Lỗi validation
            403: Không có quyền
            500: Lỗi server
        """
        try:
            data = request.get_json()
            result = self.auth_service.update_user(user_id, data)
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== DELETE USER (SUPER_ADMIN ONLY) ====================
    
    @jwt_required
    @roles_required("SUPER_ADMIN")
    def delete_user(self, user_id, **kwargs):
        """
        DELETE /api/v1/auth/users/<user_id>
        Xóa user (CHỈ SUPER_ADMIN)
        
        Headers:
            - Authorization: Bearer <access_token>
        
        Response:
            200: Xóa thành công
            400: Lỗi
            403: Không có quyền
            500: Lỗi server
        """
        try:
            result = self.auth_service.delete_user(user_id)
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
