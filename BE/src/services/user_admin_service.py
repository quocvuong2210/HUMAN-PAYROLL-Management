"""
User Admin Service - Business logic cho admin quản lý users
"""
from src.models.user_admin_model import UserAdminModel

class UserAdminService:
    def __init__(self):
        self.user_model = UserAdminModel()
    
    def get_all_users_with_roles(self):
        """
        Lấy tất cả users kèm roles
        
        Returns:
            list: Danh sách users với roles
        """
        return self.user_model.get_all_users_with_roles()
    
    def get_all_access_logs(self):
        """
        Lấy tất cả lịch sử truy cập
        
        Returns:
            list: Danh sách access logs
        """
        return self.user_model.get_all_access_logs()
