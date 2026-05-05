"""
User Admin Controller - Quản lý users với roles cho admin
"""
from flask import request, jsonify
from src.services.user_admin_service import UserAdminService
from src.utils.jwt_rbac_helper import jwt_required, roles_required

class UserAdminController:
    def __init__(self):
        self.user_service = UserAdminService()
    
    @jwt_required
    @roles_required("SUPER_ADMIN")
    def get_all_users_with_roles(self, **kwargs):
        """
        GET /api/v1/admin/users-with-roles
        Lấy tất cả users kèm roles
        
        Chỉ SUPER_ADMIN được phép
        """
        try:
            users = self.user_service.get_all_users_with_roles()
            
            return jsonify({
                "status": "success",
                "data": users
            }), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    @jwt_required
    @roles_required("SUPER_ADMIN")
    def get_all_access_logs(self, **kwargs):
        """
        GET /api/v1/admin/access-logs
        Lấy tất cả lịch sử truy cập
        
        Chỉ SUPER_ADMIN được phép
        """
        try:
            logs = self.user_service.get_all_access_logs()
            
            return jsonify({
                "status": "success",
                "data": logs
            }), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
