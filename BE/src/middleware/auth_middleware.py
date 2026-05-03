from functools import wraps
from flask import request
from src.services.auth_service import AuthService

auth_service = AuthService()

# ===== TOKEN =====
def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return {"error": "no token"}, 401

        token = token.split(" ")[1]
        user = auth_service.verify_token(token)

        if not user:
            return {"error": "invalid"}, 401

        kwargs["current_user"] = user
        return f(*args, **kwargs)
    return wrapper

# ===== RBAC =====
def has_permission(func_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = kwargs["current_user"]
            perms = auth_service.model.get_user_permissions(user)

            if func_name not in perms:
                return {"error": "RBAC forbidden"}, 403

            return f(*args, **kwargs)
        return wrapper
    return decorator

# ===== LBAC =====
def label_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = kwargs.get('current_user')
        doc_id = kwargs.get('doc_id')

        if not user:
            return {"error": "No user"}, 401

        user_label = auth_service.model.get_user_label(user)
        doc = auth_service.model.get_document(doc_id)

        if not doc:
            return {"error": "Doc not found"}, 404

        if user_label != doc["Label"]:
            return {"error": "LBAC forbidden"}, 403

        return f(*args, **kwargs)

    return wrapper