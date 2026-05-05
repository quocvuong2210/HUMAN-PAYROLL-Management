"""
Auth Model - Quản lý Authentication với Email Verification và Password Reset
"""
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash, check_password_hash
from config import SQL_SERVER_PERMISSION_CONN
from src.utils.token_generator import TokenGenerator
import datetime

class AuthModel:
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
    
    # ==================== REGISTRATION ====================
    
    def register(self, username, password, email, phone=None, dob=None, gender=None):
        """
        Đăng ký user mới với trạng thái INACTIVE
        Tạo email verification token
        
        Returns:
            tuple: (success: bool, message/user_id: str/int, token: str)
        """
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # 1. Kiểm tra username và email đã tồn tại chưa
        check_sql = """
            SELECT COUNT(*) as Count FROM [USER] 
            WHERE Username = :username OR Email = :email
        """
        check_result = self._execute(check_sql, {"username": username, "email": email}, fetch=True)
        
        if check_result[0]['Count'] > 0:
            return False, "Username hoặc Email đã tồn tại", None
        
        # 2. Insert user với status INACTIVE
        insert_sql = """
            INSERT INTO [USER] (Username, [Password], Email, PhoneNumber, DateOfBirth, Gender, [Status], EmailVerified)
            OUTPUT INSERTED.UserID
            VALUES (:username, :password, :email, :phone, :dob, :gender, 'INACTIVE', 0)
        """
        try:
            result = self._execute(insert_sql, {
                "username": username,
                "password": hashed_password,
                "email": email,
                "phone": phone,
                "dob": dob,
                "gender": gender
            }, fetch=True)
            
            user_id = result[0]['UserID']
            
            # 3. Tạo verification token (hết hạn sau 15 phút)
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
            return False, f"Lỗi đăng ký: {str(e)}", None
    
    # ==================== EMAIL VERIFICATION ====================
    
    def verify_email(self, token):
        """
        Xác nhận email bằng token
        
        Returns:
            tuple: (success: bool, message: str)
        """
        # 1. Kiểm tra token có tồn tại và chưa hết hạn
        sql = """
            SELECT UserID, ExpiredAt FROM [EmailVerification]
            WHERE Token = :token
        """
        result = self._execute(sql, {"token": token}, fetch=True)
        
        if not result:
            return False, "Token không hợp lệ"
        
        user_id = result[0]['UserID']
        expired_at = result[0]['ExpiredAt']
        
        # 2. Kiểm tra hết hạn
        if datetime.datetime.now() > expired_at:
            return False, "Token đã hết hạn"
        
        # 3. Cập nhật user status = ACTIVE và EmailVerified = 1
        try:
            update_sql = """
                UPDATE [USER]
                SET [Status] = 'ACTIVE', EmailVerified = 1
                WHERE UserID = :user_id
            """
            self._execute(update_sql, {"user_id": user_id})
            
            # 4. Xóa token đã sử dụng
            delete_sql = "DELETE FROM [EmailVerification] WHERE Token = :token"
            self._execute(delete_sql, {"token": token})
            
            return True, "Email đã được xác nhận thành công"
            
        except Exception as e:
            return False, f"Lỗi xác nhận email: {str(e)}"
    
    def resend_verification_email(self, email):
        """
        Gửi lại email xác nhận
        
        Returns:
            tuple: (success: bool, message: str, token: str, username: str)
        """
        # 1. Kiểm tra user tồn tại và chưa verify
        sql = """
            SELECT UserID, Username, EmailVerified FROM [USER]
            WHERE Email = :email
        """
        result = self._execute(sql, {"email": email}, fetch=True)
        
        if not result:
            return False, "Email không tồn tại", None, None
        
        user = result[0]
        
        if user['EmailVerified']:
            return False, "Email đã được xác nhận trước đó", None, None
        
        # 2. Xóa token cũ (nếu có)
        delete_sql = "DELETE FROM [EmailVerification] WHERE UserID = :user_id"
        self._execute(delete_sql, {"user_id": user['UserID']})
        
        # 3. Tạo token mới
        token = self.token_gen.generate_token()
        expired_at = datetime.datetime.now() + datetime.timedelta(minutes=15)
        
        insert_sql = """
            INSERT INTO [EmailVerification] (UserID, Token, ExpiredAt)
            VALUES (:user_id, :token, :expired_at)
        """
        try:
            self._execute(insert_sql, {
                "user_id": user['UserID'],
                "token": token,
                "expired_at": expired_at
            })
            
            return True, "Token mới đã được tạo", token, user['Username']
            
        except Exception as e:
            return False, f"Lỗi tạo token: {str(e)}", None, None
    
    # ==================== LOGIN ====================
    
    def login(self, username, password, ip_address, user_agent):
        """
        Đăng nhập với kiểm tra email đã xác nhận
        
        Returns:
            tuple: (success: bool, message/user_data: str/dict)
        """
        # 1. Lấy thông tin user
        sql = """
            SELECT UserID, Username, [Password], [Status], EmailVerified, Email
            FROM [USER]
            WHERE Username = :username
        """
        result = self._execute(sql, {"username": username}, fetch=True)
        
        if not result:
            return False, "Tài khoản không tồn tại"
        
        user = result[0]
        
        # 2. Kiểm tra email đã xác nhận chưa
        if not user['EmailVerified']:
            self._log_access(user['UserID'], "LOGIN_FAILED_EMAIL_NOT_VERIFIED", ip_address, user_agent)
            return False, "Email chưa được xác nhận. Vui lòng kiểm tra email của bạn."
        
        # 3. Kiểm tra trạng thái
        if user['Status'] != 'ACTIVE':
            self._log_access(user['UserID'], "LOGIN_FAILED_ACCOUNT_INACTIVE", ip_address, user_agent)
            return False, "Tài khoản của bạn đã bị khóa"
        
        # 4. Kiểm tra mật khẩu
        if check_password_hash(user['Password'], password):
            # Ghi log thành công
            self._log_access(user['UserID'], "LOGIN_SUCCESS", ip_address, user_agent)
            
            return True, {
                "user_id": user['UserID'],
                "username": user['Username'],
                "email": user['Email']
            }
        else:
            # Ghi log thất bại
            self._log_access(user['UserID'], "LOGIN_FAILED_WRONG_PASSWORD", ip_address, user_agent)
            return False, "Mật khẩu không đúng"
    
    # ==================== PASSWORD RESET ====================
    
    def create_password_reset_token(self, email):
        """
        Tạo token reset password
        
        Returns:
            tuple: (success: bool, message: str, token: str, username: str)
        """
        # 1. Kiểm tra email tồn tại
        sql = "SELECT UserID, Username FROM [USER] WHERE Email = :email"
        result = self._execute(sql, {"email": email}, fetch=True)
        
        if not result:
            return False, "Email không tồn tại trong hệ thống", None, None
        
        user = result[0]
        
        # 2. Xóa token cũ (nếu có)
        delete_sql = "DELETE FROM [PasswordReset] WHERE UserID = :user_id"
        self._execute(delete_sql, {"user_id": user['UserID']})
        
        # 3. Tạo token mới (hết hạn sau 15 phút)
        token = self.token_gen.generate_token()
        expired_at = datetime.datetime.now() + datetime.timedelta(minutes=15)
        
        insert_sql = """
            INSERT INTO [PasswordReset] (UserID, Token, ExpiredAt, IsUsed)
            VALUES (:user_id, :token, :expired_at, 0)
        """
        try:
            self._execute(insert_sql, {
                "user_id": user['UserID'],
                "token": token,
                "expired_at": expired_at
            })
            
            return True, "Token reset password đã được tạo", token, user['Username']
            
        except Exception as e:
            return False, f"Lỗi tạo token: {str(e)}", None, None
    
    def reset_password(self, token, new_password):
        """
        Reset password bằng token
        
        Returns:
            tuple: (success: bool, message: str)
        """
        # 1. Kiểm tra token
        sql = """
            SELECT UserID, ExpiredAt, IsUsed FROM [PasswordReset]
            WHERE Token = :token
        """
        result = self._execute(sql, {"token": token}, fetch=True)
        
        if not result:
            return False, "Token không hợp lệ"
        
        reset_data = result[0]
        
        # 2. Kiểm tra đã sử dụng chưa
        if reset_data['IsUsed']:
            return False, "Token đã được sử dụng"
        
        # 3. Kiểm tra hết hạn
        if datetime.datetime.now() > reset_data['ExpiredAt']:
            return False, "Token đã hết hạn"
        
        # 4. Cập nhật mật khẩu mới
        try:
            hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
            
            update_sql = """
                UPDATE [USER]
                SET [Password] = :password
                WHERE UserID = :user_id
            """
            self._execute(update_sql, {
                "password": hashed_password,
                "user_id": reset_data['UserID']
            })
            
            # 5. Đánh dấu token đã sử dụng
            mark_used_sql = """
                UPDATE [PasswordReset]
                SET IsUsed = 1
                WHERE Token = :token
            """
            self._execute(mark_used_sql, {"token": token})
            
            return True, "Mật khẩu đã được đặt lại thành công"
            
        except Exception as e:
            return False, f"Lỗi đặt lại mật khẩu: {str(e)}"
    
    # ==================== REFRESH TOKEN ====================
    
    def save_refresh_token(self, user_id, token):
        """
        Lưu refresh token vào database
        
        Returns:
            tuple: (success: bool, message: str)
        """
        expired_at = datetime.datetime.now() + datetime.timedelta(days=7)
        
        sql = """
            INSERT INTO [RefreshToken] (UserID, Token, ExpiredAt, IsRevoked)
            VALUES (:user_id, :token, :expired_at, 0)
        """
        try:
            self._execute(sql, {
                "user_id": user_id,
                "token": token,
                "expired_at": expired_at
            })
            return True, "Refresh token đã được lưu"
        except Exception as e:
            return False, f"Lỗi lưu refresh token: {str(e)}"
    
    def verify_refresh_token(self, token):
        """
        Kiểm tra refresh token có hợp lệ không
        
        Returns:
            tuple: (valid: bool, user_id: int)
        """
        sql = """
            SELECT UserID, ExpiredAt, IsRevoked FROM [RefreshToken]
            WHERE Token = :token
        """
        result = self._execute(sql, {"token": token}, fetch=True)
        
        if not result:
            return False, None
        
        token_data = result[0]
        
        # Kiểm tra revoked
        if token_data['IsRevoked']:
            return False, None
        
        # Kiểm tra hết hạn
        if datetime.datetime.now() > token_data['ExpiredAt']:
            return False, None
        
        return True, token_data['UserID']
    
    def revoke_refresh_token(self, token):
        """Thu hồi refresh token"""
        sql = "UPDATE [RefreshToken] SET IsRevoked = 1 WHERE Token = :token"
        try:
            self._execute(sql, {"token": token})
            return True, "Token đã được thu hồi"
        except Exception as e:
            return False, f"Lỗi thu hồi token: {str(e)}"
    
    def revoke_all_user_tokens(self, user_id):
        """Thu hồi tất cả refresh token của user"""
        sql = "UPDATE [RefreshToken] SET IsRevoked = 1 WHERE UserID = :user_id"
        try:
            self._execute(sql, {"user_id": user_id})
            return True, "Tất cả token đã được thu hồi"
        except Exception as e:
            return False, f"Lỗi thu hồi token: {str(e)}"
    
    # ==================== HELPER METHODS ====================
    
    def _log_access(self, user_id, action, ip, user_agent):
        """Ghi lại hành động vào bảng UserAccessLog"""
        sql = """
            INSERT INTO [UserAccessLog] (UserID, Action, IPAddress, UserAgent)
            VALUES (:uid, :action, :ip, :ua)
        """
        self._execute(sql, {"uid": user_id, "action": action, "ip": ip, "ua": user_agent})
    
    def get_user_by_id(self, user_id):
        """Lấy thông tin user"""
        sql = """
            SELECT UserID, Username, Email, PhoneNumber, DateOfBirth, Gender, Status, EmailVerified, CreatedAt
            FROM [USER]
            WHERE UserID = :user_id
        """
        result = self._execute(sql, {"user_id": user_id}, fetch=True)
        return result[0] if result else None
