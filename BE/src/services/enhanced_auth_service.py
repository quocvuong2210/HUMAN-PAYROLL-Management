"""
Enhanced Auth Service - Service layer với đầy đủ tính năng RBAC
"""
from src.models.authModel import AuthModel
from src.models.rbacModel import RBACModel
from src.utils.jwt_helper import JWTHelper
from src.utils.email_service import EmailService
from src.utils.inspector import UserInspector

class EnhancedAuthService:
    def __init__(self):
        self.auth_model = AuthModel()
        self.rbac_model = RBACModel()
        self.jwt_helper = JWTHelper()
        self.email_service = EmailService()
        self.inspector = UserInspector()
    
    # ==================== REGISTRATION ====================
    
    def register(self, data):
        """
        Đăng ký user mới
        - Tạo user với status INACTIVE
        - Tạo email verification token
        - Gửi email xác nhận
        
        Returns:
            dict: Response với status và message
        """
        # Validate input
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return {"status": "error", "message": f"Thiếu trường {field}"}
        
        # Đăng ký user
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
        
        # Gửi email xác nhận
        email_sent, email_msg = self.email_service.send_verification_email(
            to_email=data.get('email'),
            username=data.get('username'),
            token=token
        )
        
        return {
            "status": "success",
            "message": "Đăng ký thành công. Vui lòng kiểm tra email để xác nhận tài khoản.",
            "user_id": result,
            "email_sent": email_sent
        }
    
    # ==================== EMAIL VERIFICATION ====================
    
    def verify_email(self, token):
        """
        Xác nhận email bằng token
        
        Returns:
            dict: Response với status và message
        """
        success, message = self.auth_model.verify_email(token)
        
        if success:
            return {
                "status": "success",
                "message": message
            }
        
        return {
            "status": "error",
            "message": message
        }
    
    def resend_verification_email(self, email):
        """
        Gửi lại email xác nhận
        
        Returns:
            dict: Response với status và message
        """
        success, message, token, username = self.auth_model.resend_verification_email(email)
        
        if not success:
            return {"status": "error", "message": message}
        
        # Gửi email
        email_sent, email_msg = self.email_service.send_verification_email(
            to_email=email,
            username=username,
            token=token
        )
        
        return {
            "status": "success",
            "message": "Email xác nhận đã được gửi lại",
            "email_sent": email_sent
        }
    
    # ==================== LOGIN ====================
    
    def login(self, username, password, request):
        """
        Đăng nhập và tạo JWT tokens
        
        Returns:
            dict: Response với access_token và refresh_token
        """
        # Lấy thông tin request
        ip = self.inspector.get_client_ip(request)
        ua = request.user_agent.string
        
        # Xác thực
        is_authenticated, result = self.auth_model.login(username, password, ip, ua)
        
        if not is_authenticated:
            return {"status": "error", "message": result}
        
        user_data = result
        user_id = user_data['user_id']
        
        # Lấy roles của user
        roles = self.rbac_model.get_user_roles(user_id)
        role_names = [role['RoleName'] for role in roles]
        
        # Tạo access token
        access_token = self.jwt_helper.create_access_token(
            user_id=user_id,
            username=user_data['username'],
            roles=role_names
        )
        
        # Tạo refresh token
        refresh_token = self.jwt_helper.create_refresh_token(user_id)
        
        # Lưu refresh token vào database
        self.auth_model.save_refresh_token(user_id, refresh_token)
        
        return {
            "status": "success",
            "message": "Đăng nhập thành công",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "user_id": user_id,
                "username": user_data['username'],
                "email": user_data['email'],
                "roles": role_names
            }
        }
    
    # ==================== TOKEN REFRESH ====================
    
    def refresh_access_token(self, refresh_token):
        """
        Làm mới access token bằng refresh token
        
        Returns:
            dict: Response với access_token mới
        """
        # Verify refresh token từ JWT
        payload = self.jwt_helper.verify_refresh_token(refresh_token)
        
        if not payload:
            return {"status": "error", "message": "Refresh token không hợp lệ hoặc đã hết hạn"}
        
        user_id = payload.get('user_id')
        
        # Kiểm tra refresh token trong database
        is_valid, db_user_id = self.auth_model.verify_refresh_token(refresh_token)
        
        if not is_valid or db_user_id != user_id:
            return {"status": "error", "message": "Refresh token đã bị thu hồi hoặc không hợp lệ"}
        
        # Lấy thông tin user
        user = self.auth_model.get_user_by_id(user_id)
        
        if not user:
            return {"status": "error", "message": "User không tồn tại"}
        
        # Lấy roles
        roles = self.rbac_model.get_user_roles(user_id)
        role_names = [role['RoleName'] for role in roles]
        
        # Tạo access token mới
        new_access_token = self.jwt_helper.create_access_token(
            user_id=user_id,
            username=user['Username'],
            roles=role_names
        )
        
        return {
            "status": "success",
            "access_token": new_access_token
        }
    
    # ==================== LOGOUT ====================
    
    def logout(self, refresh_token):
        """
        Đăng xuất - Thu hồi refresh token
        
        Returns:
            dict: Response với status
        """
        success, message = self.auth_model.revoke_refresh_token(refresh_token)
        
        if success:
            return {"status": "success", "message": "Đăng xuất thành công"}
        
        return {"status": "error", "message": message}
    
    # ==================== PASSWORD RESET ====================
    
    def forgot_password(self, email):
        """
        Tạo token reset password và gửi email
        
        Returns:
            dict: Response với status
        """
        success, message, token, username = self.auth_model.create_password_reset_token(email)
        
        if not success:
            return {"status": "error", "message": message}
        
        # Gửi email
        email_sent, email_msg = self.email_service.send_password_reset_email(
            to_email=email,
            username=username,
            token=token
        )
        
        return {
            "status": "success",
            "message": "Email hướng dẫn đặt lại mật khẩu đã được gửi",
            "email_sent": email_sent
        }
    
    def reset_password(self, token, new_password):
        """
        Đặt lại mật khẩu bằng token
        
        Returns:
            dict: Response với status
        """
        # Validate password
        if len(new_password) < 6:
            return {"status": "error", "message": "Mật khẩu phải có ít nhất 6 ký tự"}
        
        success, message = self.auth_model.reset_password(token, new_password)
        
        if success:
            return {"status": "success", "message": message}
        
        return {"status": "error", "message": message}
    
    # ==================== USER PROFILE ====================
    
    def get_user_profile(self, user_id):
        """
        Lấy thông tin profile đầy đủ của user
        Bao gồm: thông tin cá nhân, roles, permissions
        
        Returns:
            dict: User profile data
        """
        # Lấy thông tin user
        user = self.auth_model.get_user_by_id(user_id)
        
        if not user:
            return {"status": "error", "message": "User không tồn tại"}
        
        # Lấy permissions
        permissions_info = self.rbac_model.get_user_full_permissions(user_id)
        
        return {
            "status": "success",
            "data": {
                "user_info": user,
                "roles": permissions_info['roles'],
                "permissions": permissions_info['permissions'],
                "functions": permissions_info['functions']
            }
        }
    
    # ==================== TOKEN VERIFICATION ====================
    
    def verify_access_token(self, token):
        """
        Xác thực access token
        
        Returns:
            dict: Payload nếu hợp lệ, None nếu không
        """
        return self.jwt_helper.verify_access_token(token)
    
    # ==================== RBAC ====================
    
    def check_permission(self, user_id, function_name):
        """
        Kiểm tra user có quyền thực hiện function không
        
        Returns:
            bool: True nếu có quyền
        """
        return self.rbac_model.check_user_permission(user_id, function_name)
    
    def get_user_permissions(self, user_id):
        """
        Lấy danh sách tất cả function mà user có quyền
        
        Returns:
            list: Danh sách function names
        """
        return self.rbac_model.get_user_permissions(user_id)
