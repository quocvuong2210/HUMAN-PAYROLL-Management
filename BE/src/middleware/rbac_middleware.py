"""
RBAC Middleware - Middleware kiểm tra quyền truy cập
"""
from functools import wraps
from flask import request, jsonify
from src.services.enhanced_auth_service import EnhancedAuthService

auth_service = EnhancedAuthService()

def token_required(f):
    """
    Decorator yêu cầu access token hợp lệ
    Thêm user_id và payload vào kwargs
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Lấy token từ header
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return jsonify({
                "status": "error",
                "message": "Thiếu token xác thực"
            }), 401
        
        # Kiểm tra format Bearer token
        if not auth_header.startswith("Bearer "):
            return jsonify({
                "status": "error",
                "message": "Format token không hợp lệ. Sử dụng: Bearer <token>"
            }), 401
        
        token = auth_header.split(" ")[1]
        
        # Verify token
        payload = auth_service.verify_access_token(token)
        
        if not payload:
            return jsonify({
                "status": "error",
                "message": "Token không hợp lệ hoặc đã hết hạn"
            }), 401
        
        # Thêm thông tin user vào kwargs
        kwargs["current_user_id"] = payload.get("user_id")
        kwargs["current_username"] = payload.get("username")
        kwargs["current_user_roles"] = payload.get("roles", [])
        kwargs["token_payload"] = payload
        
        return f(*args, **kwargs)
    
    return wrapper


def require_permission(function_name):
    """
    Decorator kiểm tra quyền thực hiện function cụ thể
    Phải sử dụng sau @token_required
    
    Usage:
        @token_required
        @require_permission("USER_EDIT")
        def update_user():
            ...
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Lấy user_id từ kwargs (được thêm bởi @token_required)
            user_id = kwargs.get("current_user_id")
            
            if not user_id:
                return jsonify({
                    "status": "error",
                    "message": "Không tìm thấy thông tin user. Vui lòng sử dụng @token_required trước."
                }), 401
            
            # Kiểm tra quyền
            has_permission = auth_service.check_permission(user_id, function_name)
            
            if not has_permission:
                return jsonify({
                    "status": "error",
                    "message": f"Bạn không có quyền thực hiện chức năng này ({function_name})"
                }), 403
            
            return f(*args, **kwargs)
        
        return wrapper
    return decorator


def require_any_permission(*function_names):
    """
    Decorator kiểm tra user có ít nhất 1 trong các quyền được liệt kê
    
    Usage:
        @token_required
        @require_any_permission("USER_VIEW", "USER_EDIT")
        def view_user():
            ...
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id = kwargs.get("current_user_id")
            
            if not user_id:
                return jsonify({
                    "status": "error",
                    "message": "Không tìm thấy thông tin user"
                }), 401
            
            # Kiểm tra có ít nhất 1 quyền
            for func_name in function_names:
                if auth_service.check_permission(user_id, func_name):
                    return f(*args, **kwargs)
            
            return jsonify({
                "status": "error",
                "message": f"Bạn không có quyền thực hiện chức năng này. Cần một trong: {', '.join(function_names)}"
            }), 403
        
        return wrapper
    return decorator


def require_all_permissions(*function_names):
    """
    Decorator kiểm tra user có tất cả các quyền được liệt kê
    
    Usage:
        @token_required
        @require_all_permissions("USER_VIEW", "USER_EDIT")
        def admin_action():
            ...
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id = kwargs.get("current_user_id")
            
            if not user_id:
                return jsonify({
                    "status": "error",
                    "message": "Không tìm thấy thông tin user"
                }), 401
            
            # Kiểm tra tất cả quyền
            for func_name in function_names:
                if not auth_service.check_permission(user_id, func_name):
                    return jsonify({
                        "status": "error",
                        "message": f"Bạn thiếu quyền: {func_name}"
                    }), 403
            
            return f(*args, **kwargs)
        
        return wrapper
    return decorator


def require_role(*role_names):
    """
    Decorator kiểm tra user có role cụ thể
    
    Usage:
        @token_required
        @require_role("ADMIN", "HR_MANAGER")
        def admin_only():
            ...
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_roles = kwargs.get("current_user_roles", [])
            
            # Kiểm tra có ít nhất 1 role phù hợp
            for role in role_names:
                if role in user_roles:
                    return f(*args, **kwargs)
            
            return jsonify({
                "status": "error",
                "message": f"Bạn không có vai trò phù hợp. Cần một trong: {', '.join(role_names)}"
            }), 403
        
        return wrapper
    return decorator


def optional_auth(f):
    """
    Decorator cho phép truy cập cả khi có hoặc không có token
    Nếu có token hợp lệ, thêm thông tin user vào kwargs
    
    Usage:
        @optional_auth
        def public_endpoint():
            # current_user_id sẽ là None nếu không có token
            ...
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        
        # Không có token - cho phép truy cập
        if not auth_header or not auth_header.startswith("Bearer "):
            kwargs["current_user_id"] = None
            kwargs["current_username"] = None
            kwargs["current_user_roles"] = []
            return f(*args, **kwargs)
        
        # Có token - verify
        token = auth_header.split(" ")[1]
        payload = auth_service.verify_access_token(token)
        
        if payload:
            kwargs["current_user_id"] = payload.get("user_id")
            kwargs["current_username"] = payload.get("username")
            kwargs["current_user_roles"] = payload.get("roles", [])
            kwargs["token_payload"] = payload
        else:
            kwargs["current_user_id"] = None
            kwargs["current_username"] = None
            kwargs["current_user_roles"] = []
        
        return f(*args, **kwargs)
    
    return wrapper
