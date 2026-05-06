"""
Token Generator - Tạo random token đơn giản
"""
import secrets

class TokenGenerator:
    @staticmethod
    def generate_token(length=32):
        """
        Tạo token ngẫu nhiên
        
        Args:
            length: Độ dài token (default 32)
        
        Returns:
            str: Token string
        """
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_numeric_token(length=6):
        """
        Tạo token số (dùng cho OTP)
        
        Args:
            length: Độ dài (default 6)
        
        Returns:
            str: Numeric token
        """
        return ''.join([str(secrets.randbelow(10)) for _ in range(length)])
