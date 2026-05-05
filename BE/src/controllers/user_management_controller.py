"""
User Management Controller - Quản lý người dùng với RBAC
"""
from flask import jsonify, request
from src.services.user_management_service import UserManagementService

class UserManagementController:
    def __init__(self):
        self.service = UserManagementService()
    
    # ==================== USER CRUD ====================
    
    def create_user(self, current_user_id, **kwargs):
        """
        POST /users/create
        Tạo user mới và gán roles
        (Yêu cầu @token_required và @require_permission("USER_CREATE"))
        
        Body:
            - username (required)
            - email (required)
            - password (required)
            - phone (optional)
            - dob (optional)
            - gender (optional)
            - roles (required): [1, 2, 3] - Array of RoleIDs
        """
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['username', 'email', 'password', 'roles']
            for field in required_fields:
                if field not in data:
                    return jsonify({
                        "status": "error",
                        "message": f"Thiếu trường bắt buộc: {field}"
                    }), 400
            
            # Validate roles is array
            if not isinstance(data['roles'], list) or len(data['roles']) == 0:
                return jsonify({
                    "status": "error",
                    "message": "Roles phải là mảng và không được rỗng"
                }), 400
            
            result = self.service.create_user_with_roles(data, current_user_id)
            
            status_code = 201 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def get_all_users(self, current_user_id, **kwargs):
        """
        GET /users
        Lấy danh sách tất cả users
        (Yêu cầu @token_required và @require_permission("USER_VIEW"))
        """
        try:
            result = self.service.get_all_users()
            return jsonify(result), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def get_user_by_id(self, user_id, current_user_id, **kwargs):
        """
        GET /users/{user_id}
        Lấy thông tin chi tiết user
        (Yêu cầu @token_required và @require_permission("USER_VIEW"))
        """
        try:
            result = self.service.get_user_detail(user_id)
            
            status_code = 200 if result["status"] == "success" else 404
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def update_user(self, user_id, current_user_id, **kwargs):
        """
        PUT /users/{user_id}
        Cập nhật thông tin user
        (Yêu cầu @token_required và @require_permission("USER_EDIT"))
        
        Body:
            - username (optional)
            - email (optional)
            - phone (optional)
            - dob (optional)
            - gender (optional)
            - status (optional)
        """
        try:
            data = request.get_json()
            result = self.service.update_user(user_id, data)
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def delete_user(self, user_id, current_user_id, **kwargs):
        """
        DELETE /users/{user_id}
        Xóa user
        (Yêu cầu @token_required và @require_permission("USER_DELETE"))
        """
        try:
            result = self.service.delete_user(user_id)
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== USER ROLES MANAGEMENT ====================
    
    def update_user_roles(self, user_id, current_user_id, **kwargs):
        """
        PUT /users/{user_id}/roles
        Cập nhật roles của user
        (Yêu cầu @token_required và @require_permission("USER_EDIT"))
        
        Body:
            - roles: [1, 2, 3] - Array of RoleIDs
        """
        try:
            data = request.get_json()
            
            if 'roles' not in data or not isinstance(data['roles'], list):
                return jsonify({
                    "status": "error",
                    "message": "Roles phải là mảng"
                }), 400
            
            result = self.service.update_user_roles(user_id, data['roles'])
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def add_role_to_user(self, user_id, current_user_id, **kwargs):
        """
        POST /users/{user_id}/roles
        Thêm role cho user
        (Yêu cầu @token_required và @require_permission("USER_EDIT"))
        
        Body:
            - role_id (required)
        """
        try:
            data = request.get_json()
            
            if 'role_id' not in data:
                return jsonify({
                    "status": "error",
                    "message": "Thiếu role_id"
                }), 400
            
            result = self.service.add_role_to_user(user_id, data['role_id'])
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def remove_role_from_user(self, user_id, role_id, current_user_id, **kwargs):
        """
        DELETE /users/{user_id}/roles/{role_id}
        Xóa role khỏi user
        (Yêu cầu @token_required và @require_permission("USER_EDIT"))
        """
        try:
            result = self.service.remove_role_from_user(user_id, role_id)
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
