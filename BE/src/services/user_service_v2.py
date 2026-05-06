"""
User Service V2 - Production-Ready User Management with RBAC
Business logic for user creation with roles, email verification, and activity logging
"""
from src.models.user_model_v2 import UserModelV2
from src.models.roleModel import RoleModel
import bcrypt
import datetime

class UserServiceV2:
    def __init__(self):
        self.user_model = UserModelV2()
        self.role_model = RoleModel()
    
    def create_user_with_roles(self, username, email, password, phone_number, 
                               date_of_birth, gender, role_ids, ip_address, user_agent):
        """
        Tạo user mới với roles
        
        Logic:
        1. Validate input
        2. Hash password với bcrypt
        3. Insert vào bảng USER với Status='INACTIVE'
        4. Nếu roleIds rỗng → gán role EMPLOYEE (default)
        5. Insert vào bảng USER_ROLE
        6. Tạo EmailVerification token (15 phút)
        7. Log activity: CREATE_USER
        8. Return user_id, verification_token
        
        Args:
            username: Tên đăng nhập
            email: Email
            password: Mật khẩu (chưa hash)
            phone_number: Số điện thoại (optional)
            date_of_birth: Ngày sinh (optional)
            gender: Giới tính (optional)
            role_ids: List role IDs (optional - default EMPLOYEE)
            ip_address: IP address
            user_agent: User agent
        
        Returns:
            tuple: (success: bool, result: dict/str)
        """
        try:
            # 1. Validate email format
            if not self._validate_email(email):
                return False, "Email không hợp lệ"
            
            # 2. Validate password length
            if len(password) < 6:
                return False, "Mật khẩu phải có ít nhất 6 ký tự"
            
            # 3. Validate username length
            if len(username) < 3:
                return False, "Tên đăng nhập phải có ít nhất 3 ký tự"
            
            # 4. Check if username or email already exists
            if self.user_model.check_user_exists(username, email):
                return False, "Tên đăng nhập hoặc email đã tồn tại"
            
            # 5. Hash password với bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # 6. If no roles provided, get EMPLOYEE role ID as default
            if not role_ids or len(role_ids) == 0:
                employee_role = self.user_model.get_role_id_by_name('EMPLOYEE')
                if employee_role:
                    role_ids = [employee_role]
                else:
                    # Fallback: create with no roles (will need manual assignment)
                    role_ids = []
            
            # 7. Create user in database
            success, user_id, verification_token = self.user_model.create_user(
                username=username,
                email=email,
                password=hashed_password,
                phone_number=phone_number,
                date_of_birth=date_of_birth,
                gender=gender,
                status='INACTIVE'
            )
            
            if not success:
                return False, user_id  # user_id contains error message
            
            # 8. Assign roles to user
            if role_ids:
                role_success, role_message = self.user_model.assign_roles_to_user(user_id, role_ids)
                if not role_success:
                    # Rollback: delete user if role assignment fails
                    self.user_model.delete_user(user_id)
                    return False, f"Lỗi gán vai trò: {role_message}"
            
            # 9. Get assigned role names
            assigned_roles = self.user_model.get_user_role_names(user_id)
            
            # 10. Log activity
            self.user_model.log_activity(
                user_id=user_id,
                action='CREATE_USER',
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            # 11. Return success with user data
            return True, {
                "user_id": user_id,
                "username": username,
                "email": email,
                "status": "INACTIVE",
                "roles": assigned_roles,
                "verification_token": verification_token,
                "verification_expires_in": "15 minutes"
            }
            
        except Exception as e:
            return False, f"Lỗi tạo người dùng: {str(e)}"
    
    def get_all_roles(self):
        """
        Lấy danh sách tất cả roles
        
        Returns:
            list: Danh sách roles
        """
        return self.role_model.get_all_roles()
    
    def verify_email(self, token):
        """
        Xác nhận email bằng token
        
        Args:
            token: Verification token
        
        Returns:
            tuple: (success: bool, message: str)
        """
        return self.user_model.verify_email(token)
    
    def resend_verification_email(self, email):
        """
        Gửi lại email xác nhận
        
        Args:
            email: Email address
        
        Returns:
            tuple: (success: bool, message: str, token: str)
        """
        return self.user_model.resend_verification_email(email)
    
    def _validate_email(self, email):
        """
        Validate email format
        
        Args:
            email: Email address
        
        Returns:
            bool: True if valid, False otherwise
        """
        import re
        pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        return re.match(pattern, email) is not None
