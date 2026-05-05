"""
JWT RBAC Helper - JWT với Roles, Permissions, Functions
"""
import jwt
import datetime
import os
from dotenv import load_dotenv
from functools import wraps
from flask import request, jsonify

load_dotenv()

class JWTRBACHelper:
    def __init__(self):
        self.secret_key = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this-in-production')
        self.algorithm = "HS256"
        
        # Get expiration times from env (in seconds)
        access_expires_seconds = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 hour
        refresh_expires_seconds = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 2592000))  # 30 days
        
        self.access_token_expires = datetime.timedelta(seconds=access_expires_seconds)
        self.refresh_token_expires = datetime.timedelta(seconds=refresh_expires_seconds)
    
    def create_access_token(self, user_id, username, email, roles=None, permissions=None, functions=None):
        """
        Tạo Access Token với RBAC đầy đủ
        
        Args:
            user_id: User ID
            username: Username
            email: Email
            roles: List of role names
            permissions: List of permission names
            functions: List of function names
        
        Returns:
            str: JWT access token
        """
        payload = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "roles": roles or [],
            "permissions": permissions or [],
            "functions": functions or [],
            "type": "access",
            "exp": datetime.datetime.utcnow() + self.access_token_expires,
            "iat": datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def create_refresh_token(self, user_id):
        """
        Tạo Refresh Token
        
        Args:
            user_id: User ID
        
        Returns:
            str: JWT refresh token
        """
        payload = {
            "user_id": user_id,
            "type": "refresh",
            "exp": datetime.datetime.utcnow() + self.refresh_token_expires,
            "iat": datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def verify_access_token(self, token):
        """
        Xác thực Access Token
        
        Args:
            token: JWT token
        
        Returns:
            dict: Payload if valid, None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            if payload.get("type") != "access":
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def verify_refresh_token(self, token):
        """
        Xác thực Refresh Token
        
        Args:
            token: Refresh token
        
        Returns:
            dict: Payload if valid, None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            if payload.get("type") != "refresh":
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def decode_without_verification(self, token):
        """
        Giải mã token không xác thực (for debugging)
        
        Args:
            token: JWT token
        
        Returns:
            dict: Payload
        """
        try:
            return jwt.decode(token, options={"verify_signature": False})
        except Exception as e:
            return {"error": str(e)}


# ==================== DECORATORS ====================

jwt_helper = JWTRBACHelper()

def jwt_required(f):
    """
    Decorator yêu cầu JWT token hợp lệ
    Thêm payload vào kwargs
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Allow OPTIONS requests without authentication (for CORS preflight)
        if request.method == 'OPTIONS':
            return '', 200
        
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return jsonify({
                "status": "error",
                "message": "Thiếu token xác thực"
            }), 401
        
        if not auth_header.startswith("Bearer "):
            return jsonify({
                "status": "error",
                "message": "Format token không hợp lệ. Sử dụng: Bearer <token>"
            }), 401
        
        token = auth_header.split(" ")[1]
        payload = jwt_helper.verify_access_token(token)
        
        if not payload:
            return jsonify({
                "status": "error",
                "message": "Token không hợp lệ hoặc đã hết hạn"
            }), 401
        
        # Thêm payload vào kwargs
        kwargs["jwt_payload"] = payload
        kwargs["current_user_id"] = payload.get("user_id")
        kwargs["current_username"] = payload.get("username")
        kwargs["current_user_roles"] = payload.get("roles", [])
        kwargs["current_user_permissions"] = payload.get("permissions", [])
        kwargs["current_user_functions"] = payload.get("functions", [])
        
        return f(*args, **kwargs)
    
    return wrapper


def roles_required(*required_roles):
    """
    Decorator kiểm tra user có role yêu cầu
    Phải dùng sau @jwt_required
    
    Usage:
        @jwt_required
        @roles_required("SUPER_ADMIN", "HR_MANAGER")
        def admin_only():
            pass
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Allow OPTIONS requests without authentication (for CORS preflight)
            if request.method == 'OPTIONS':
                return '', 200
            
            user_roles = kwargs.get("current_user_roles", [])
            
            # Check if user has any of the required roles
            has_role = any(role in user_roles for role in required_roles)
            
            if not has_role:
                return jsonify({
                    "status": "error",
                    "message": f"Bạn không có quyền truy cập. Cần một trong các vai trò: {', '.join(required_roles)}"
                }), 403
            
            return f(*args, **kwargs)
        
        return wrapper
    return decorator


def permissions_required(*required_permissions):
    """
    Decorator kiểm tra user có permission yêu cầu
    Phải dùng sau @jwt_required
    
    Usage:
        @jwt_required
        @permissions_required("USER_MANAGEMENT", "HR_MANAGEMENT")
        def manage_users():
            pass
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_permissions = kwargs.get("current_user_permissions", [])
            
            # Check if user has any of the required permissions
            has_permission = any(perm in user_permissions for perm in required_permissions)
            
            if not has_permission:
                return jsonify({
                    "status": "error",
                    "message": f"Bạn không có quyền thực hiện hành động này. Cần một trong các quyền: {', '.join(required_permissions)}"
                }), 403
            
            return f(*args, **kwargs)
        
        return wrapper
    return decorator


def functions_required(*required_functions):
    """
    Decorator kiểm tra user có function yêu cầu
    Phải dùng sau @jwt_required
    
    Usage:
        @jwt_required
        @functions_required("USER_EDIT", "USER_DELETE")
        def edit_user():
            pass
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_functions = kwargs.get("current_user_functions", [])
            
            # Check if user has any of the required functions
            has_function = any(func in user_functions for func in required_functions)
            
            if not has_function:
                return jsonify({
                    "status": "error",
                    "message": f"Bạn không có quyền thực hiện chức năng này. Cần một trong: {', '.join(required_functions)}"
                }), 403
            
            return f(*args, **kwargs)
        
        return wrapper
    return decorator


def optional_jwt(f):
    """
    Decorator cho phép truy cập cả khi có hoặc không có token
    Nếu có token hợp lệ, thêm thông tin user vào kwargs
    
    Usage:
        @optional_jwt
        def public_endpoint():
            # current_user_id sẽ là None nếu không có token
            pass
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            kwargs["jwt_payload"] = None
            kwargs["current_user_id"] = None
            kwargs["current_username"] = None
            kwargs["current_user_roles"] = []
            kwargs["current_user_permissions"] = []
            kwargs["current_user_functions"] = []
            return f(*args, **kwargs)
        
        token = auth_header.split(" ")[1]
        payload = jwt_helper.verify_access_token(token)
        
        if payload:
            kwargs["jwt_payload"] = payload
            kwargs["current_user_id"] = payload.get("user_id")
            kwargs["current_username"] = payload.get("username")
            kwargs["current_user_roles"] = payload.get("roles", [])
            kwargs["current_user_permissions"] = payload.get("permissions", [])
            kwargs["current_user_functions"] = payload.get("functions", [])
        else:
            kwargs["jwt_payload"] = None
            kwargs["current_user_id"] = None
            kwargs["current_username"] = None
            kwargs["current_user_roles"] = []
            kwargs["current_user_permissions"] = []
            kwargs["current_user_functions"] = []
        
        return f(*args, **kwargs)
    
    return wrapper
