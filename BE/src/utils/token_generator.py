"""
Token Generator - Tạo random token cho email verification và password reset
"""
import secrets
import string

class TokenGenerator:
    @staticmethod
    def generate_token(length=64):
        """
        Tạo random token an toàn
        
        Args:
            length: Độ dài token (default: 64)
            
        Returns:
            str: Random token
        """
        # Sử dụng secrets module (cryptographically strong)
        alphabet = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(alphabet) for _ in range(length))
        return token
    
    @staticmethod
    def generate_numeric_token(length=6):
        """
        Tạo token số (dùng cho OTP)
        
        Args:
            length: Độ dài token (default: 6)
            
        Returns:
            str: Numeric token
        """
        return ''.join(secrets.choice(string.digits) for _ in range(length))
