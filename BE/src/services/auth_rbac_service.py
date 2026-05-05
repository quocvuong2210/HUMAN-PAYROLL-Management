"""
Auth RBAC Service - Service xử lý authentication với RBAC
"""
from src.models.userModel import UserModel
from src.models.rbacModel import RBACModel
from src.utils.jwt_rbac_helper import JWTRBACHelper
from src.utils.inspector import UserInspector

class AuthRBACService:
    def __init__(self):
        self.user_model = UserModel()
        self.rbac_model = RBACModel()
        self.jwt_helper = JWTRBACHelper()
        self.inspector = UserInspector()
    
    # ==================== REGISTRATION ====================
    
    def register(self, data):
        """
        Đăng ký user mới
        
        Args:
            data: Dict chứa username, email, password, phone, dob, gender
        
        Returns:
            dict: Response với status và message
        """
        success, message = self.user_model.register(
            username=data.get('username'),
            password=data.get('password'),
            email=data.get('email'),
            phone=data.get('phone'),
            dob=data.get('dob'),
            gender=data.get('gender')
        )
        
        if success:
            return {
                "status": "success",
                "message": "Đăng ký thành công. Bạn có thể đăng nhập ngay."
            }
        
        return {
            "status": "error",
            "message": message
        }
    
    # ==================== LOGIN ====================
    
    def login(self, username, password, request):
        """
        Đăng nhập và tạo JWT tokens với roles
        
        Args:
            username: Tên đăng nhập
            password: Mật khẩu
            request: Flask request object
        
        Returns:
            dict: Response với token và user info
        """
        # Lấy IP và User Agent
        ip = self.inspector.get_client_ip(request)
        ua = request.user_agent.string
        
        # Xác thực
        is_authenticated, result = self.user_model.login(username, password, ip, ua)
        
        if not is_authenticated:
            return {
                "status": "error",
                "message": result
            }
        
        user_id = result
        
        # Lấy thông tin user
        user_info = self.user_model.get_user_by_id(user_id)
        
        if user_info["status"] != "success":
            return {
                "status": "error",
                "message": "Không tìm thấy thông tin user"
            }
        
        user_data = user_info["data"]
        
        # Lấy roles, permissions, functions của user
        permissions_info = self.rbac_model.get_user_full_permissions(user_id)
        
        roles = permissions_info['roles']
        permissions = permissions_info['permissions']
        functions = permissions_info['functions']  # This is already a list of strings
        
        role_names = [role['RoleName'] for role in roles]
        permission_names = [perm['PermissionName'] for perm in permissions]
        function_names = functions  # Already a list of strings, no need to extract
        
        # Tạo access token với roles, permissions, functions
        access_token = self.jwt_helper.create_access_token(
            user_id=user_id,
            username=user_data['Username'],
            email=user_data['Email'],
            roles=role_names,
            permissions=permission_names,
            functions=function_names
        )
        
        # Tạo refresh token
        refresh_token = self.jwt_helper.create_refresh_token(user_id)
        
        return {
            "status": "success",
            "message": "Đăng nhập thành công",
            "token": access_token,
            "refreshToken": refresh_token,
            "user": {
                "userId": user_id,
                "username": user_data['Username'],
                "email": user_data['Email'],
                "roles": role_names,
                "permissions": permission_names,
                "functions": function_names
            }
        }
    
    # ==================== REFRESH TOKEN ====================
    
    def refresh_access_token(self, refresh_token):
        """
        Làm mới access token
        
        Args:
            refresh_token: Refresh token
        
        Returns:
            dict: Response với access token mới
        """
        # Verify refresh token
        payload = self.jwt_helper.verify_refresh_token(refresh_token)
        
        if not payload:
            return {
                "status": "error",
                "message": "Refresh token không hợp lệ hoặc đã hết hạn"
            }
        
        user_id = payload.get('user_id')
        
        # Lấy thông tin user
        user_info = self.user_model.get_user_by_id(user_id)
        
        if user_info["status"] != "success":
            return {
                "status": "error",
                "message": "User không tồn tại"
            }
        
        user_data = user_info["data"]
        
        # Lấy roles, permissions, functions
        permissions_info = self.rbac_model.get_user_full_permissions(user_id)
        
        roles = permissions_info['roles']
        permissions = permissions_info['permissions']
        functions = permissions_info['functions']  # Already a list of strings
        
        role_names = [role['RoleName'] for role in roles]
        permission_names = [perm['PermissionName'] for perm in permissions]
        function_names = functions  # Already a list of strings
        
        # Tạo access token mới
        new_access_token = self.jwt_helper.create_access_token(
            user_id=user_id,
            username=user_data['Username'],
            email=user_data['Email'],
            roles=role_names,
            permissions=permission_names,
            functions=function_names
        )
        
        return {
            "status": "success",
            "token": new_access_token
        }
    
    # ==================== LOGOUT ====================
    
    def logout(self, refresh_token=None):
        """
        Đăng xuất
        
        Args:
            refresh_token: Optional refresh token để thu hồi
        
        Returns:
            dict: Response
        """
        # TODO: Implement refresh token revocation in database
        # For now, just return success
        return {
            "status": "success",
            "message": "Đăng xuất thành công"
        }
    
    # ==================== USER PROFILE ====================
    
    def get_user_profile(self, user_id):
        """
        Lấy thông tin profile đầy đủ
        
        Args:
            user_id: User ID
        
        Returns:
            dict: User profile với roles, permissions, functions
        """
        # Lấy thông tin user
        user_info = self.user_model.get_user_by_id(user_id)
        
        if user_info["status"] != "success":
            return {
                "status": "error",
                "message": "User không tồn tại"
            }
        
        user_data = user_info["data"]
        
        # Lấy roles, permissions, functions
        permissions_info = self.rbac_model.get_user_full_permissions(user_id)
        
        return {
            "status": "success",
            "data": {
                "userId": user_data['UserID'],
                "username": user_data['Username'],
                "email": user_data['Email'],
                "phone": user_data.get('PhoneNumber'),
                "dob": str(user_data.get('DateOfBirth')) if user_data.get('DateOfBirth') else None,
                "gender": user_data.get('Gender'),
                "status": user_data.get('Status'),
                "createdAt": str(user_data.get('CreatedAt')) if user_data.get('CreatedAt') else None,
                "roles": permissions_info['roles'],
                "permissions": permissions_info['permissions'],
                "functions": permissions_info['functions']
            }
        }
    
    # ==================== CHANGE PASSWORD ====================
    
    def change_password(self, user_id, old_password, new_password):
        """
        Đổi mật khẩu
        
        Args:
            user_id: User ID
            old_password: Mật khẩu cũ
            new_password: Mật khẩu mới
        
        Returns:
            dict: Response
        """
        success, message = self.user_model.change_password(user_id, old_password, new_password)
        
        if success:
            return {
                "status": "success",
                "message": message
            }
        
        return {
            "status": "error",
            "message": message
        }
    
    # ==================== UPDATE PROFILE ====================
    
    def update_user_profile(self, user_id, data):
        """
        Cập nhật profile của user hiện tại
        
        Args:
            user_id: User ID
            data: Dict chứa email, phone, dob, gender
        
        Returns:
            dict: Response
        """
        success, message = self.user_model.update_user(
            user_id=user_id,
            username=None,  # Không cho phép đổi username
            email=data.get('email'),
            phone=data.get('phone'),
            dob=data.get('dob'),
            gender=data.get('gender'),
            status=None  # Không cho phép tự đổi status
        )
        
        if success:
            # Lấy lại thông tin user sau khi update
            user_info = self.get_user_profile(user_id)
            return {
                "status": "success",
                "message": "Cập nhật profile thành công",
                "data": user_info.get("data")
            }
        
        return {
            "status": "error",
            "message": message
        }
    
    # ==================== GET USER ACCESS LOGS ====================
    
    def get_user_access_logs(self, user_id, limit=50):
        """
        Lấy lịch sử truy cập của user
        
        Args:
            user_id: User ID
            limit: Số lượng logs (default: 50)
        
        Returns:
            dict: Response với danh sách logs
        """
        from sqlalchemy import create_engine, text
        from config import SQL_SERVER_PERMISSION_CONN
        
        try:
            engine = create_engine(SQL_SERVER_PERMISSION_CONN)
            
            sql = """
                SELECT TOP (:limit)
                    LogID,
                    UserID,
                    Action,
                    IPAddress,
                    UserAgent,
                    AccessTime
                FROM ACCESS_LOG
                WHERE UserID = :user_id
                ORDER BY AccessTime DESC
            """
            
            with engine.connect() as conn:
                result = conn.execute(text(sql), {"user_id": user_id, "limit": limit})
                rows = result.fetchall()
                
                logs = []
                for row in rows:
                    logs.append({
                        "LogID": row[0],
                        "UserID": row[1],
                        "Action": row[2],
                        "IPAddress": row[3],
                        "UserAgent": row[4],
                        "AccessTime": str(row[5]) if row[5] else None
                    })
                
                return {
                    "status": "success",
                    "data": logs,
                    "count": len(logs)
                }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Lỗi lấy access logs: {str(e)}"
            }
    
    # ==================== CREATE USER WITH ROLES (ADMIN) ====================
    
    def create_user_with_roles(self, data):
        """
        Tạo user mới và gán roles (CHỈ SUPER_ADMIN)
        
        Args:
            data: Dict chứa user info và roleIds
        
        Returns:
            dict: Response
        """
        # 1. Tạo user
        success, message = self.user_model.register(
            username=data.get('username'),
            password=data.get('password'),
            email=data.get('email'),
            phone=data.get('phone'),
            dob=data.get('dob'),
            gender=data.get('gender')
        )
        
        if not success:
            return {
                "status": "error",
                "message": message
            }
        
        # 2. Lấy user_id vừa tạo
        sql = "SELECT UserID FROM [USER] WHERE Username = :username"
        from sqlalchemy import create_engine, text
        from config import SQL_SERVER_PERMISSION_CONN
        
        engine = create_engine(SQL_SERVER_PERMISSION_CONN)
        with engine.connect() as conn:
            result = conn.execute(text(sql), {"username": data.get('username')})
            row = result.fetchone()
            user_id = row[0] if row else None
        
        if not user_id:
            return {
                "status": "error",
                "message": "Không tìm thấy user vừa tạo"
            }
        
        # 3. Gán roles nếu có
        role_ids = data.get('roleIds', [])
        assigned_roles = []
        
        for role_id in role_ids:
            success, msg = self.rbac_model.assign_role_to_user(user_id, role_id)
            if success:
                # Lấy role name
                role_info = self.rbac_model.get_role_by_id(role_id)
                if role_info:
                    assigned_roles.append(role_info['RoleName'])
        
        return {
            "status": "success",
            "message": "Tạo user thành công",
            "data": {
                "userId": user_id,
                "username": data.get('username'),
                "email": data.get('email'),
                "roles": assigned_roles
            }
        }
    
    # ==================== UPDATE USER (ADMIN) ====================
    
    def update_user(self, user_id, data):
        """
        Cập nhật thông tin user
        
        Args:
            user_id: User ID
            data: Dict chứa thông tin cần update
        
        Returns:
            dict: Response
        """
        success, message = self.user_model.update_user(
            user_id=user_id,
            username=data.get('username'),
            email=data.get('email'),
            phone=data.get('phone'),
            dob=data.get('dob'),
            gender=data.get('gender'),
            status=data.get('status')
        )
        
        if success:
            return {
                "status": "success",
                "message": message
            }
        
        return {
            "status": "error",
            "message": message
        }
    
    # ==================== DELETE USER (ADMIN) ====================
    
    def delete_user(self, user_id):
        """
        Xóa user
        
        Args:
            user_id: User ID
        
        Returns:
            dict: Response
        """
        success, message = self.user_model.delete_user(user_id)
        
        if success:
            return {
                "status": "success",
                "message": message
            }
        
        return {
            "status": "error",
            "message": message
        }
