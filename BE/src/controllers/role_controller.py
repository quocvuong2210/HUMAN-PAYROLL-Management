"""
Role Controller - Quản lý vai trò người dùng
"""
from flask import jsonify, request
from src.models.roleModel import RoleModel

class RoleController:
    def __init__(self):
        self.model = RoleModel()
    
    def get_all_roles(self):
        """Lấy danh sách tất cả roles"""
        try:
            roles = self.model.get_all_roles()
            return jsonify({
                "status": "success",
                "data": roles
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    def get_user_roles(self, user_id):
        """Lấy danh sách roles của user"""
        try:
            roles = self.model.get_user_roles(user_id)
            return jsonify({
                "status": "success",
                "data": roles
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    def update_user_roles(self, user_id):
        """Cập nhật roles của user"""
        try:
            data = request.get_json()
            roles = data.get('roles', [])
            
            if not isinstance(roles, list):
                return jsonify({
                    "status": "error",
                    "message": "Roles phải là mảng"
                }), 400
            
            success, message = self.model.update_user_roles(user_id, roles)
            
            if success:
                return jsonify({
                    "status": "success",
                    "message": message
                }), 200
            else:
                return jsonify({
                    "status": "error",
                    "message": message
                }), 400
                
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    def get_role_permissions(self, role_id):
        """Lấy danh sách permissions của role"""
        try:
            permissions = self.model.get_role_permissions(role_id)
            return jsonify({
                "status": "success",
                "data": permissions
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
