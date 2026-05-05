"""
JWT Helper - Quản lý Access Token và Refresh Token
"""
import jwt
import datetime
import os

class JWTHelper:
    def __init__(self):
        # Lấy secret key từ environment (Production nên dùng key phức tạp)
        self.access_secret = os.getenv('JWT_ACCESS_SECRET', 'your-access-secret-key-change-in-production')
        self.refresh_secret = os.getenv('JWT_REFRESH_SECRET', 'your-refresh-secret-key-change-in-production')
        
        # Thời gian hết hạn
        self.access_token_expire_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 15))
        self.refresh_token_expire_days = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS', 7))
    
    def create_access_token(self, user_id, username, roles=None):
        """
        Tạo Access Token (JWT)
        
        Args:
            user_id: ID người dùng
            username: Tên đăng nhập
            roles: Danh sách vai trò (optional)
            
        Returns:
            str: JWT token
        """
        payload = {
            "user_id": user_id,
            "username": username,
            "roles": roles or [],
            "type": "access",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=self.access_token_expire_minutes),
            "iat": datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.access_secret, algorithm="HS256")
        return token
    
    def create_refresh_token(self, user_id):
        """
        Tạo Refresh Token
        
        Args:
            user_id: ID người dùng
            
        Returns:
            str: JWT refresh token
        """
        payload = {
            "user_id": user_id,
            "type": "refresh",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=self.refresh_token_expire_days),
            "iat": datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.refresh_secret, algorithm="HS256")
        return token
    
    def verify_access_token(self, token):
        """
        Xác thực Access Token
        
        Args:
            token: JWT token cần xác thực
            
        Returns:
            dict: Payload nếu hợp lệ, None nếu không hợp lệ
        """
        try:
            payload = jwt.decode(token, self.access_secret, algorithms=["HS256"])
            
            # Kiểm tra loại token
            if payload.get("type") != "access":
                return None
                
            return payload
            
        except jwt.ExpiredSignatureError:
            return None  # Token hết hạn
        except jwt.InvalidTokenError:
            return None  # Token không hợp lệ
    
    def verify_refresh_token(self, token):
        """
        Xác thực Refresh Token
        
        Args:
            token: Refresh token cần xác thực
            
        Returns:
            dict: Payload nếu hợp lệ, None nếu không hợp lệ
        """
        try:
            payload = jwt.decode(token, self.refresh_secret, algorithms=["HS256"])
            
            # Kiểm tra loại token
            if payload.get("type") != "refresh":
                return None
                
            return payload
            
        except jwt.ExpiredSignatureError:
            return None  # Token hết hạn
        except jwt.InvalidTokenError:
            return None  # Token không hợp lệ
    
    def decode_token_without_verification(self, token):
        """
        Giải mã token mà không xác thực (dùng cho debug)
        
        Args:
            token: JWT token
            
        Returns:
            dict: Payload
        """
        try:
            return jwt.decode(token, options={"verify_signature": False})
        except Exception as e:
            return {"error": str(e)}
