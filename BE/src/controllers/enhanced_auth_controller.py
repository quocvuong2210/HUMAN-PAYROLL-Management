"""
Enhanced Auth Controller - Controller xử lý các API authentication và RBAC
"""
from flask import jsonify, request
from src.services.enhanced_auth_service import EnhancedAuthService
from src.models.rbacModel import RBACModel

class EnhancedAuthController:
    def __init__(self):
        self.auth_service = EnhancedAuthService()
        self.rbac_model = RBACModel()
    
    # ==================== AUTHENTICATION ====================
    
    def register(self):
        """
        POST /auth/register
        Đăng ký user mới
        
        Body:
            - username (required)
            - email (required)
            - password (required)
            - phone (optional)
            - dob (optional)
            - gender (optional)
        """
        try:
            data = request.get_json()
            result = self.auth_service.register(data)
            
            status_code = 201 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def verify_email(self):
        """
        GET /auth/verify-email?token=xxx
        Xác nhận email
        """
        try:
            token = request.args.get('token')
            
            if not token:
                return jsonify({
                    "status": "error",
                    "message": "Thiếu token xác nhận"
                }), 400
            
            result = self.auth_service.verify_email(token)
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def resend_verification(self):
        """
        POST /auth/resend-verification
        Gửi lại email xác nhận
        
        Body:
            - email (required)
        """
        try:
            data = request.get_json()
            email = data.get('email')
            
            if not email:
                return jsonify({
                    "status": "error",
                    "message": "Thiếu email"
                }), 400
            
            result = self.auth_service.resend_verification_email(email)
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def login(self):
        """
        POST /auth/login
        Đăng nhập
        
        Body:
            - username (required)
            - password (required)
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
            
            result = self.auth_service.login(username, password, request)
            
            status_code = 200 if result["status"] == "success" else 401
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def refresh_token(self):
        """
        POST /auth/refresh-token
        Làm mới access token
        
        Body:
            - refresh_token (required)
        """
        try:
            data = request.get_json()
            refresh_token = data.get('refresh_token')
            
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
    
    def logout(self):
        """
        POST /auth/logout
        Đăng xuất (thu hồi refresh token)
        
        Body:
            - refresh_token (required)
        """
        try:
            data = request.get_json()
            refresh_token = data.get('refresh_token')
            
            if not refresh_token:
                return jsonify({
                    "status": "error",
                    "message": "Thiếu refresh token"
                }), 400
            
            result = self.auth_service.logout(refresh_token)
            
            return jsonify(result), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== PASSWORD MANAGEMENT ====================
    
    def forgot_password(self):
        """
        POST /auth/forgot-password
        Yêu cầu reset password
        
        Body:
            - email (required)
        """
        try:
            data = request.get_json()
            email = data.get('email')
            
            if not email:
                return jsonify({
                    "status": "error",
                    "message": "Thiếu email"
                }), 400
            
            result = self.auth_service.forgot_password(email)
            
            return jsonify(result), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def reset_password(self):
        """
        POST /auth/reset-password
        Đặt lại mật khẩu bằng token
        
        Body:
            - token (required)
            - new_password (required)
        """
        try:
            data = request.get_json()
            token = data.get('token')
            new_password = data.get('new_password')
            
            if not token or not new_password:
                return jsonify({
                    "status": "error",
                    "message": "Thiếu token hoặc mật khẩu mới"
                }), 400
            
            result = self.auth_service.reset_password(token, new_password)
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== USER PROFILE ====================
    
    def get_profile(self, current_user_id, **kwargs):
        """
        GET /users/me
        Lấy thông tin profile của user hiện tại
        (Yêu cầu @token_required)
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
    
    def get_my_permissions(self, current_user_id, **kwargs):
        """
        GET /users/me/permissions
        Lấy danh sách quyền của user hiện tại
        (Yêu cầu @token_required)
        """
        try:
            permissions = self.auth_service.get_user_permissions(current_user_id)
            
            return jsonify({
                "status": "success",
                "data": {
                    "user_id": current_user_id,
                    "permissions": permissions
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== ADMIN - USER MANAGEMENT ====================
    
    def assign_role(self, current_user_id, **kwargs):
        """
        POST /admin/users/assign-role
        Gán role cho user
        (Yêu cầu @token_required và @require_permission("USER_EDIT"))
        
        Body:
            - user_id (required)
            - role_id (required)
        """
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            role_id = data.get('role_id')
            
            if not user_id or not role_id:
                return jsonify({
                    "status": "error",
                    "message": "Thiếu user_id hoặc role_id"
                }), 400
            
            success, message = self.rbac_model.assign_role_to_user(user_id, role_id)
            
            if success:
                return jsonify({
                    "status": "success",
                    "message": message
                }), 200
            
            return jsonify({
                "status": "error",
                "message": message
            }), 400
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def remove_role(self, current_user_id, **kwargs):
        """
        POST /admin/users/remove-role
        Xóa role khỏi user
        (Yêu cầu @token_required và @require_permission("USER_EDIT"))
        
        Body:
            - user_id (required)
            - role_id (required)
        """
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            role_id = data.get('role_id')
            
            if not user_id or not role_id:
                return jsonify({
                    "status": "error",
                    "message": "Thiếu user_id hoặc role_id"
                }), 400
            
            success, message = self.rbac_model.remove_role_from_user(user_id, role_id)
            
            if success:
                return jsonify({
                    "status": "success",
                    "message": message
                }), 200
            
            return jsonify({
                "status": "error",
                "message": message
            }), 400
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def get_user_roles(self, user_id):
        """
        GET /admin/users/{user_id}/roles
        Lấy danh sách role của user
        (Yêu cầu @token_required và @require_permission("USER_VIEW"))
        """
        try:
            roles = self.rbac_model.get_user_roles(user_id)
            
            return jsonify({
                "status": "success",
                "data": {
                    "user_id": user_id,
                    "roles": roles
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== ADMIN - RBAC MANAGEMENT ====================
    
    def get_all_roles(self, current_user_id, **kwargs):
        """
        GET /admin/roles
        Lấy danh sách tất cả roles
        (Yêu cầu @token_required)
        """
        try:
            roles = self.rbac_model.get_all_roles()
            
            return jsonify({
                "status": "success",
                "data": roles
            }), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def get_all_permissions(self, current_user_id, **kwargs):
        """
        GET /admin/permissions
        Lấy danh sách tất cả permissions
        (Yêu cầu @token_required)
        """
        try:
            permissions = self.rbac_model.get_all_permissions()
            
            return jsonify({
                "status": "success",
                "data": permissions
            }), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def get_all_functions(self, current_user_id, **kwargs):
        """
        GET /admin/functions
        Lấy danh sách tất cả system functions
        (Yêu cầu @token_required)
        """
        try:
            functions = self.rbac_model.get_all_functions()
            
            return jsonify({
                "status": "success",
                "data": functions
            }), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
