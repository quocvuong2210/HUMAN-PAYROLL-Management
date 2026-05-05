"""
OTP Model - Quản lý OTP verification
"""
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class OTPModel:
    def __init__(self):
        self.engine = create_engine(SQL_SERVER_PERMISSION_CONN)
        self.otp_expire_minutes = int(os.getenv('OTP_EXPIRE_MINUTES', 5))
        self.resend_cooldown = int(os.getenv('OTP_RESEND_COOLDOWN_SECONDS', 60))
    
    def _execute(self, sql, params=None, fetch=False):
        """Hàm thực thi truy vấn nội bộ"""
        with self.engine.connect() as conn:
            with conn.begin():
                query = text(sql)
                result = conn.execute(query, params or {})
                if fetch:
                    return [dict(row._mapping) for row in result.fetchall()]
                return result
    
    def save_otp(self, email, otp_code):
        """
        Lưu OTP vào database
        
        Args:
            email: Email address
            otp_code: OTP code
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # 1. Xóa OTP cũ của email này (nếu có)
            delete_sql = "DELETE FROM [OTP_VERIFICATION] WHERE Email = :email"
            self._execute(delete_sql, {"email": email})
            
            # 2. Tạo OTP mới
            expired_at = datetime.now() + timedelta(minutes=self.otp_expire_minutes)
            
            insert_sql = """
                INSERT INTO [OTP_VERIFICATION] (Email, OTPCode, ExpiredAt, IsUsed)
                VALUES (:email, :otp_code, :expired_at, 0)
            """
            self._execute(insert_sql, {
                "email": email,
                "otp_code": otp_code,
                "expired_at": expired_at
            })
            
            return True, "OTP đã được lưu"
            
        except Exception as e:
            return False, f"Lỗi lưu OTP: {str(e)}"
    
    def verify_otp(self, email, otp_code):
        """
        Xác thực OTP
        
        Args:
            email: Email address
            otp_code: OTP code to verify
        
        Returns:
            tuple: (valid: bool, message: str)
        """
        try:
            # 1. Tìm OTP hợp lệ
            sql = """
                SELECT * FROM [OTP_VERIFICATION]
                WHERE Email = :email
                  AND OTPCode = :otp_code
                  AND ExpiredAt > GETDATE()
                  AND IsUsed = 0
            """
            result = self._execute(sql, {
                "email": email,
                "otp_code": otp_code
            }, fetch=True)
            
            if not result:
                # Check if OTP exists but expired or used
                check_sql = """
                    SELECT * FROM [OTP_VERIFICATION]
                    WHERE Email = :email AND OTPCode = :otp_code
                """
                check_result = self._execute(check_sql, {
                    "email": email,
                    "otp_code": otp_code
                }, fetch=True)
                
                if check_result:
                    otp = check_result[0]
                    if otp['IsUsed']:
                        return False, "Mã OTP đã được sử dụng"
                    elif otp['ExpiredAt'] < datetime.now():
                        return False, "Mã OTP đã hết hạn"
                
                return False, "Mã OTP không hợp lệ"
            
            # 2. Đánh dấu OTP đã sử dụng
            update_sql = """
                UPDATE [OTP_VERIFICATION]
                SET IsUsed = 1, UsedAt = GETDATE()
                WHERE Email = :email AND OTPCode = :otp_code
            """
            self._execute(update_sql, {
                "email": email,
                "otp_code": otp_code
            })
            
            return True, "Xác thực OTP thành công"
            
        except Exception as e:
            return False, f"Lỗi xác thực OTP: {str(e)}"
    
    def check_resend_cooldown(self, email, ip_address=None):
        """
        Kiểm tra có thể resend OTP không (cooldown)
        
        Args:
            email: Email address
            ip_address: IP address (optional)
        
        Returns:
            tuple: (can_resend: bool, seconds_remaining: int, message: str)
        """
        try:
            # 1. Lấy lần request cuối cùng
            sql = """
                SELECT TOP 1 RequestedAt
                FROM [OTP_RESEND_LOG]
                WHERE Email = :email
                ORDER BY RequestedAt DESC
            """
            result = self._execute(sql, {"email": email}, fetch=True)
            
            if not result:
                # Chưa có request nào -> cho phép
                return True, 0, "Có thể gửi OTP"
            
            last_request = result[0]['RequestedAt']
            seconds_passed = (datetime.now() - last_request).total_seconds()
            
            if seconds_passed >= self.resend_cooldown:
                return True, 0, "Có thể gửi OTP"
            else:
                seconds_remaining = int(self.resend_cooldown - seconds_passed)
                return False, seconds_remaining, f"Vui lòng đợi {seconds_remaining} giây trước khi gửi lại"
            
        except Exception as e:
            # Nếu có lỗi, cho phép gửi (fail-open)
            return True, 0, "Có thể gửi OTP"
    
    def log_resend_request(self, email, ip_address=None):
        """
        Ghi log resend request
        
        Args:
            email: Email address
            ip_address: IP address (optional)
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            sql = """
                INSERT INTO [OTP_RESEND_LOG] (Email, IPAddress, RequestedAt)
                VALUES (:email, :ip, GETDATE())
            """
            self._execute(sql, {
                "email": email,
                "ip": ip_address
            })
            
            return True, "Đã ghi log resend"
            
        except Exception as e:
            return False, f"Lỗi ghi log: {str(e)}"
    
    def cleanup_expired_otp(self):
        """
        Xóa OTP đã hết hạn hoặc đã sử dụng
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Xóa OTP hết hạn hoặc đã dùng
            sql = """
                DELETE FROM [OTP_VERIFICATION]
                WHERE ExpiredAt < GETDATE() OR IsUsed = 1
            """
            self._execute(sql)
            
            # Xóa log cũ (> 24h)
            log_sql = """
                DELETE FROM [OTP_RESEND_LOG]
                WHERE RequestedAt < DATEADD(HOUR, -24, GETDATE())
            """
            self._execute(log_sql)
            
            return True, "Đã dọn dẹp OTP cũ"
            
        except Exception as e:
            return False, f"Lỗi dọn dẹp: {str(e)}"
    
    def get_otp_stats(self, email):
        """
        Lấy thống kê OTP của email
        
        Args:
            email: Email address
        
        Returns:
            dict: Statistics
        """
        try:
            sql = """
                SELECT 
                    COUNT(*) as TotalOTP,
                    SUM(CASE WHEN IsUsed = 1 THEN 1 ELSE 0 END) as UsedOTP,
                    SUM(CASE WHEN ExpiredAt < GETDATE() AND IsUsed = 0 THEN 1 ELSE 0 END) as ExpiredOTP,
                    MAX(CreatedAt) as LastOTPTime
                FROM [OTP_VERIFICATION]
                WHERE Email = :email
            """
            result = self._execute(sql, {"email": email}, fetch=True)
            
            if result:
                return result[0]
            return None
            
        except Exception as e:
            return None
