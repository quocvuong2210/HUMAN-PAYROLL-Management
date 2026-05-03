from flask import request, jsonify
from src.models.permisstionModel import PermissionModel

class PermissionController:
    def __init__(self):
        self.model = PermissionModel()

    def get_permissions(self, user_id):
        """Lấy quyền của user"""
        permissions = self.model.get_user_permissions(user_id)
        return jsonify({"status": "success", "permissions": permissions}), 200

    def check_access(self, user_id, function_name):
        """Kiểm tra quyền truy cập một chức năng cụ thể"""
        has_access = self.model.check_user_access(user_id, function_name)
        return jsonify({"status": "success", "has_access": has_access}), 200

    def assign_role(self):
        """Gán vai trò cho user"""
        data = request.get_json()
        user_id = data.get("user_id")
        role_id = data.get("role_id")
        
        success, message = self.model.assign_role_to_user(user_id, role_id)
        if success:
            return jsonify({"status": "success", "message": message}), 200
        return jsonify({"status": "error", "message": message}), 400