"""
User Model V2 - Production-Ready User Management with RBAC
Database operations for user creation with roles, email verification, and activity logging
"""
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN
from src.utils.token_generator import TokenGenerator
import datetime

class UserModelV2:
    def __init__(self):
        self.engine = create_engine(SQL_SERVER_PERMISSION_CONN)
        self.token_gen = TokenGenerator()
    
    def _execute(self, sql, params=None, fetch=False):
        """Hàm thực thi truy vấn nội bộ"""
        with self.engine.connect() as conn:
            with conn.begin():
                query = text(sql)
                result = conn.execute(query, params or {})
                if fetch:
                    return [dict(row._mapping) for row in result.fetchall()]
                return result
    
    def check_user_exists(self, username, email):
        """
        Kiểm tra username hoặc email đã tồn tại chưa
        
        Args:
            username: Tên đăng nhập
            email: Email
        
        Returns:
            bool: True nếu đã tồn tại, False nếu chưa
        """
        sql = """
            SELECT COUNT(*) as Count FROM [USER]
            WHERE Username = :username OR Email = :email
        """
        result = self._execute(sql, {"username": username, "email": email}, fetch=True)
        return result[0]['Count'] > 0
    
    def get_role_id_by_name(self, role_name):
        """
        Lấy RoleID từ RoleName
        
        Args:
            role_name: Tên role (VD: 'EMPLOYEE')
        
        Returns:
            int: RoleID hoặc None nếu không tìm thấy
        """
        sql = "SELECT RoleID FROM [ROLE] WHERE RoleName = :role_name"
        result = self._execute(sql, {"role_name": role_name}, fetch=True)
        return result[0]['RoleID'] if result else None
    
    def create_user(self, username, email, password, phone_number, date_of_birth, gender, status):
        """
        Tạo user mới trong database
        
        Args:
            username: Tên đăng nhập
            email: Email
            password: Mật khẩu đã hash
            phone_number: Số điện thoại
            date_of_birth: Ngày sinh
            gender: Giới tính
            status: Trạng thái (INACTIVE/ACTIVE)
        
        Returns:
            tuple: (success: bool, user_id/error: int/str, verification_token: str)
        """
        try:
            # 1. Insert user
            insert_sql = """
                INSERT INTO [USER] (Username, [Password], Email, PhoneNumber, DateOfBirth, Gender, [Status], EmailVerified)
                OUTPUT INSERTED.UserID
                VALUES (:username, :password, :email, :phone, :dob, :gender, :status, 0)
            """
            result = self._execute(insert_sql, {
                "username": username,
                "password": password,
                "email": email,
                "phone": phone_number,
                "dob": date_of_birth,
                "gender": gender,
                "status": status
            }, fetch=True)
            
            user_id = result[0]['UserID']
            
            # 2. Create email verification token (expires in 15 minutes)
            token = self.token_gen.generate_token()
            expired_at = datetime.datetime.now() + datetime.timedelta(minutes=15)
            
            token_sql = """
                INSERT INTO [EmailVerification] (UserID, Token, ExpiredAt)
                VALUES (:user_id, :token, :expired_at)
            """
            self._execute(token_sql, {
                "user_id": user_id,
                "token": token,
                "expired_at": expired_at
            })
            
            return True, user_id, token
            
        except Exception as e:
            return False, f"Lỗi tạo user: {str(e)}", None
    
    def assign_roles_to_user(self, user_id, role_ids):
        """
        Gán roles cho user
        
        Args:
            user_id: User ID
            role_ids: List of role IDs
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            for role_id in role_ids:
                sql = """
                    INSERT INTO [USER_ROLE] (UserID, RoleID)
                    VALUES (:user_id, :role_id)
                """
                self._execute(sql, {
                    "user_id": user_id,
                    "role_id": role_id
                })
            
            return True, "Gán vai trò thành công"
            
        except Exception as e:
            return False, f"Lỗi gán vai trò: {str(e)}"
    
    def get_user_role_names(self, user_id):
        """
        Lấy danh sách tên roles của user
        
        Args:
            user_id: User ID
        
        Returns:
            list: Danh sách tên roles
        """
        sql = """
            SELECT R.RoleName
            FROM [USER_ROLE] UR
            INNER JOIN [ROLE] R ON UR.RoleID = R.RoleID
            WHERE UR.UserID = :user_id
            ORDER BY R.RoleID
        """
        result = self._execute(sql, {"user_id": user_id}, fetch=True)
        return [row['RoleName'] for row in result]
    
    def verify_email(self, token):
        """
        Xác nhận email bằng token
        
        Args:
            token: Verification token
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # 1. Check if token exists and not expired
            sql = """
                SELECT UserID, ExpiredAt FROM [EmailVerification]
                WHERE Token = :token
            """
            result = self._execute(sql, {"token": token}, fetch=True)
            
            if not result:
                return False, "Token không hợp lệ"
            
            user_id = result[0]['UserID']
            expired_at = result[0]['ExpiredAt']
            
            # 2. Check if expired
            if datetime.datetime.now() > expired_at:
                return False, "Token đã hết hạn. Vui lòng yêu cầu gửi lại email xác nhận."
            
            # 3. Update user status to ACTIVE and EmailVerified to 1
            update_sql = """
                UPDATE [USER]
                SET [Status] = 'ACTIVE', EmailVerified = 1
                WHERE UserID = :user_id
            """
            self._execute(update_sql, {"user_id": user_id})
            
            # 4. Delete used token
            delete_sql = "DELETE FROM [EmailVerification] WHERE Token = :token"
            self._execute(delete_sql, {"token": token})
            
            # 5. Log activity
            self.log_activity(user_id, 'EMAIL_VERIFIED', None, None)
            
            return True, "Email đã được xác nhận thành công. Bạn có thể đăng nhập ngay bây giờ."
            
        except Exception as e:
            return False, f"Lỗi xác nhận email: {str(e)}"
    
    def resend_verification_email(self, email):
        """
        Gửi lại email xác nhận
        
        Args:
            email: Email address
        
        Returns:
            tuple: (success: bool, message: str, token: str)
        """
        try:
            # 1. Check if user exists and not verified
            sql = """
                SELECT UserID, Username, EmailVerified FROM [USER]
                WHERE Email = :email
            """
            result = self._execute(sql, {"email": email}, fetch=True)
            
            if not result:
                return False, "Email không tồn tại trong hệ thống", None
            
            user = result[0]
            
            if user['EmailVerified']:
                return False, "Email đã được xác nhận trước đó", None
            
            # 2. Delete old tokens
            delete_sql = "DELETE FROM [EmailVerification] WHERE UserID = :user_id"
            self._execute(delete_sql, {"user_id": user['UserID']})
            
            # 3. Create new token
            token = self.token_gen.generate_token()
            expired_at = datetime.datetime.now() + datetime.timedelta(minutes=15)
            
            insert_sql = """
                INSERT INTO [EmailVerification] (UserID, Token, ExpiredAt)
                VALUES (:user_id, :token, :expired_at)
            """
            self._execute(insert_sql, {
                "user_id": user['UserID'],
                "token": token,
                "expired_at": expired_at
            })
            
            return True, "Email xác nhận đã được gửi lại", token
            
        except Exception as e:
            return False, f"Lỗi gửi lại email: {str(e)}", None
    
    def log_activity(self, user_id, action, ip_address, user_agent):
        """
        Ghi log hoạt động vào bảng UserAccessLog
        
        Args:
            user_id: User ID
            action: Hành động (CREATE_USER, LOGIN, UPDATE_USER, etc.)
            ip_address: IP address
            user_agent: User agent
        """
        try:
            sql = """
                INSERT INTO [UserAccessLog] (UserID, Action, IPAddress, UserAgent)
                VALUES (:user_id, :action, :ip, :ua)
            """
            self._execute(sql, {
                "user_id": user_id,
                "action": action,
                "ip": ip_address,
                "ua": user_agent
            })
        except Exception as e:
            # Log error but don't fail the main operation
            print(f"Warning: Failed to log activity: {str(e)}")
    
    def delete_user(self, user_id):
        """
        Xóa user (rollback khi tạo user thất bại)
        
        Args:
            user_id: User ID
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            sql = "DELETE FROM [USER] WHERE UserID = :user_id"
            self._execute(sql, {"user_id": user_id})
            return True, "Xóa user thành công"
        except Exception as e:
            return False, f"Lỗi xóa user: {str(e)}"
