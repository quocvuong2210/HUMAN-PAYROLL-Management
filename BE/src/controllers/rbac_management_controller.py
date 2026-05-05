"""
RBAC Management Controller - Quản lý Role, Permission, Function
"""
from flask import jsonify, request
from src.services.rbac_management_service import RBACManagementService

class RBACManagementController:
    def __init__(self):
        self.service = RBACManagementService()
    
    # ==================== ROLE PERMISSIONS ====================
    
    def get_role_permissions(self, role_id, current_user_id, **kwargs):
        """
        GET /rbac/roles/{role_id}/permissions
        Lấy danh sách permissions của role
        """
        try:
            result = self.service.get_role_permissions(role_id)
            return jsonify(result), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def update_role_permissions(self, role_id, current_user_id, **kwargs):
        """
        PUT /rbac/roles/{role_id}/permissions
        Cập nhật permissions của role
        (Yêu cầu @token_required và @require_role("ADMIN"))
        
        Body:
            - permission_ids: [1, 2, 3] - Array of PermissionIDs
        """
        try:
            data = request.get_json()
            
            if 'permission_ids' not in data or not isinstance(data['permission_ids'], list):
                return jsonify({
                    "status": "error",
                    "message": "permission_ids phải là mảng"
                }), 400
            
            result = self.service.update_role_permissions(role_id, data['permission_ids'])
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def add_permission_to_role(self, role_id, current_user_id, **kwargs):
        """
        POST /rbac/roles/{role_id}/permissions
        Thêm permission cho role
        (Yêu cầu @token_required và @require_role("ADMIN"))
        
        Body:
            - permission_id (required)
        """
        try:
            data = request.get_json()
            
            if 'permission_id' not in data:
                return jsonify({
                    "status": "error",
                    "message": "Thiếu permission_id"
                }), 400
            
            result = self.service.add_permission_to_role(role_id, data['permission_id'])
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def remove_permission_from_role(self, role_id, permission_id, current_user_id, **kwargs):
        """
        DELETE /rbac/roles/{role_id}/permissions/{permission_id}
        Xóa permission khỏi role
        (Yêu cầu @token_required và @require_role("ADMIN"))
        """
        try:
            result = self.service.remove_permission_from_role(role_id, permission_id)
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== PERMISSION FUNCTIONS ====================
    
    def get_permission_functions(self, permission_id, current_user_id, **kwargs):
        """
        GET /rbac/permissions/{permission_id}/functions
        Lấy danh sách functions của permission
        """
        try:
            result = self.service.get_permission_functions(permission_id)
            return jsonify(result), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== ROLE MANAGEMENT ====================
    
    def create_role(self, current_user_id, **kwargs):
        """
        POST /rbac/roles
        Tạo role mới
        (Yêu cầu @token_required và @require_role("ADMIN"))
        
        Body:
            - role_name (required)
            - description (optional)
        """
        try:
            data = request.get_json()
            
            if 'role_name' not in data:
                return jsonify({
                    "status": "error",
                    "message": "Thiếu role_name"
                }), 400
            
            result = self.service.create_role(
                data['role_name'],
                data.get('description')
            )
            
            status_code = 201 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def update_role(self, role_id, current_user_id, **kwargs):
        """
        PUT /rbac/roles/{role_id}
        Cập nhật thông tin role
        (Yêu cầu @token_required và @require_role("ADMIN"))
        
        Body:
            - role_name (optional)
            - description (optional)
        """
        try:
            data = request.get_json()
            result = self.service.update_role(role_id, data)
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def delete_role(self, role_id, current_user_id, **kwargs):
        """
        DELETE /rbac/roles/{role_id}
        Xóa role
        (Yêu cầu @token_required và @require_role("ADMIN"))
        """
        try:
            result = self.service.delete_role(role_id)
            
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    # ==================== STATISTICS ====================
    
    def get_rbac_statistics(self, current_user_id, **kwargs):
        """
        GET /rbac/statistics
        Lấy thống kê RBAC
        (Yêu cầu @token_required)
        """
        try:
            result = self.service.get_statistics()
            return jsonify(result), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
