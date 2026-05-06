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
        users = self.user_model.get_all_users_with_roles()
        
        # Format datetime fields to include timezone info
        for user in users:
            if user.get('CreatedAt'):
                dt = user['CreatedAt']
                user['CreatedAt'] = dt.strftime('%Y-%m-%dT%H:%M:%S') + '+07:00'
            
            if user.get('LastLoginAt'):
                dt = user['LastLoginAt']
                user['LastLoginAt'] = dt.strftime('%Y-%m-%dT%H:%M:%S') + '+07:00'
            
            if user.get('DateOfBirth') and hasattr(user['DateOfBirth'], 'strftime'):
                user['DateOfBirth'] = user['DateOfBirth'].strftime('%Y-%m-%d')
        
        return users
    
    def get_all_access_logs(self):
        """
        Lấy tất cả lịch sử truy cập
        
        Returns:
            list: Danh sách access logs
        """
        logs = self.user_model.get_all_access_logs()
        
        # Format datetime to include timezone info
        for log in logs:
            if log.get('AccessTime'):
                # Convert datetime to ISO format string with timezone
                # Assume server time is GMT+7 (Vietnam)
                dt = log['AccessTime']
                # Format as ISO string with +07:00 timezone
                log['AccessTime'] = dt.strftime('%Y-%m-%dT%H:%M:%S') + '+07:00'
        
        return logs
