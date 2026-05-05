"""
User Management Service - Business logic cho quản lý user
"""
from src.models.authModel import AuthModel
from src.models.rbacModel import RBACModel
from src.utils.email_service import EmailService

class UserManagementService:
    def __init__(self):
        self.auth_model = AuthModel()
        self.rbac_model = RBACModel()
        self.email_service = EmailService()
    
    def create_user_with_roles(self, data, created_by_user_id):
        """
        Tạo user mới và gán roles
        
        Args:
            data: dict chứa thông tin user và roles
            created_by_user_id: ID của user tạo
            
        Returns:
            dict: Response với status và message
        """
        # 1. Tạo user (sẽ tự động tạo verification token)
        success, result, token = self.auth_model.register(
            username=data.get('username'),
            password=data.get('password'),
            email=data.get('email'),
            phone=data.get('phone'),
            dob=data.get('dob'),
            gender=data.get('gender')
        )
        
        if not success:
            return {"status": "error", "message": result}
        
        user_id = result
        
        # 2. Gán roles cho user
        roles = data.get('roles', [])
        assigned_roles = []
        failed_roles = []
        
        for role_id in roles:
            success, message = self.rbac_model.assign_role_to_user(user_id, role_id)
            if success:
                assigned_roles.append(role_id)
            else:
                failed_roles.append({"role_id": role_id, "error": message})
        
        # 3. Gửi email verification (optional)
        try:
            self.email_service.send_verification_email(
                to_email=data.get('email'),
                username=data.get('username'),
                token=token
            )
        except Exception as e:
            print(f"Warning: Could not send verification email: {str(e)}")
        
        return {
            "status": "success",
            "message": "Tạo người dùng thành công",
            "data": {
                "user_id": user_id,
                "username": data.get('username'),
                "email": data.get('email'),
                "assigned_roles": assigned_roles,
                "failed_roles": failed_roles,
                "verification_token": token
            }
        }
    
    def get_all_users(self):
        """
        Lấy danh sách tất cả users
        
        Returns:
            dict: Response với danh sách users
        """
        from src.models.userModel import UserModel
        user_model = UserModel()
        
        users = user_model.get_all_users()
        
        return {
            "status": "success",
            "data": users
        }
    
    def get_user_detail(self, user_id):
        """
        Lấy thông tin chi tiết user kèm roles và permissions
        
        Args:
            user_id: ID của user
            
        Returns:
            dict: Response với thông tin user
        """
        # Lấy thông tin user
        user = self.auth_model.get_user_by_id(user_id)
        
        if not user:
            return {"status": "error", "message": "User không tồn tại"}
        
        # Lấy roles
        roles = self.rbac_model.get_user_roles(user_id)
        
        # Lấy permissions
        permissions_info = self.rbac_model.get_user_full_permissions(user_id)
        
        return {
            "status": "success",
            "data": {
                "user_info": user,
                "roles": roles,
                "permissions": permissions_info['permissions'],
                "functions": permissions_info['functions']
            }
        }
    
    def update_user(self, user_id, data):
        """
        Cập nhật thông tin user
        
        Args:
            user_id: ID của user
            data: dict chứa thông tin cần update
            
        Returns:
            dict: Response với status
        """
        from src.models.userModel import UserModel
        user_model = UserModel()
        
        success, message = user_model.update_user(
            user_id=user_id,
            username=data.get('username'),
            email=data.get('email'),
            phone=data.get('phone'),
            dob=data.get('dob'),
            gender=data.get('gender'),
            status=data.get('status')
        )
        
        if success:
            return {"status": "success", "message": message}
        
        return {"status": "error", "message": message}
    
    def delete_user(self, user_id):
        """
        Xóa user
        
        Args:
            user_id: ID của user
            
        Returns:
            dict: Response với status
        """
        from src.models.userModel import UserModel
        user_model = UserModel()
        
        success, message = user_model.delete_user(user_id)
        
        if success:
            return {"status": "success", "message": message}
        
        return {"status": "error", "message": message}
    
    # ==================== ROLE MANAGEMENT ====================
    
    def update_user_roles(self, user_id, role_ids):
        """
        Cập nhật toàn bộ roles của user
        (Xóa tất cả roles cũ và gán roles mới)
        
        Args:
            user_id: ID của user
            role_ids: List các RoleID mới
            
        Returns:
            dict: Response với status
        """
        # 1. Lấy roles hiện tại
        current_roles = self.rbac_model.get_user_roles(user_id)
        current_role_ids = [role['RoleID'] for role in current_roles]
        
        # 2. Xóa roles cũ
        for role_id in current_role_ids:
            self.rbac_model.remove_role_from_user(user_id, role_id)
        
        # 3. Thêm roles mới
        assigned_roles = []
        failed_roles = []
        
        for role_id in role_ids:
            success, message = self.rbac_model.assign_role_to_user(user_id, role_id)
            if success:
                assigned_roles.append(role_id)
            else:
                failed_roles.append({"role_id": role_id, "error": message})
        
        return {
            "status": "success",
            "message": "Cập nhật roles thành công",
            "data": {
                "assigned_roles": assigned_roles,
                "failed_roles": failed_roles
            }
        }
    
    def add_role_to_user(self, user_id, role_id):
        """
        Thêm role cho user
        
        Args:
            user_id: ID của user
            role_id: ID của role
            
        Returns:
            dict: Response với status
        """
        success, message = self.rbac_model.assign_role_to_user(user_id, role_id)
        
        if success:
            return {"status": "success", "message": message}
        
        return {"status": "error", "message": message}
    
    def remove_role_from_user(self, user_id, role_id):
        """
        Xóa role khỏi user
        
        Args:
            user_id: ID của user
            role_id: ID của role
            
        Returns:
            dict: Response với status
        """
        success, message = self.rbac_model.remove_role_from_user(user_id, role_id)
        
        if success:
            return {"status": "success", "message": message}
        
        return {"status": "error", "message": message}
