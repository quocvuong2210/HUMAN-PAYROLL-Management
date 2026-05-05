"""
User Controller V2 - Production-Ready User Management with RBAC
Handles user creation with role assignment, email verification, and activity logging
"""
from flask import jsonify, request
from src.services.user_service_v2 import UserServiceV2
from src.middleware.rbac_middleware import token_required, require_permission

class UserControllerV2:
    def __init__(self):
        self.user_service = UserServiceV2()
    
    def create_user_with_roles(self):
        """
        API: POST /api/v1/auth/users
        Tạo user mới với roles
        
        Body:
        {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "password123",
            "phoneNumber": "0123456789",
            "dateOfBirth": "1990-01-01",
            "gender": "Nam",
            "roleIds": [1, 2]  // Optional - default to EMPLOYEE if empty
        }
        
        Returns:
        {
            "status": "success",
            "message": "Tạo người dùng thành công",
            "data": {
                "user_id": 123,
                "username": "john_doe",
                "email": "john@example.com",
                "status": "INACTIVE",
                "roles": ["HR_MANAGER", "EMPLOYEE"],
                "verification_token": "abc123...",
                "verification_expires_in": "15 minutes"
            }
        }
        """
        try:
            data = request.get_json()
            
            # Validate required fields
            required = ['username', 'email', 'password']
            if not data or not all(k in data for k in required):
                return jsonify({
                    "status": "error",
                    "message": "Thiếu thông tin bắt buộc (username, email, password)"
                }), 400
            
            # Extract data
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            phone_number = data.get('phoneNumber')
            date_of_birth = data.get('dateOfBirth')
            gender = data.get('gender')
            role_ids = data.get('roleIds', [])  # Default to empty list
            
            # Get IP and User Agent for logging
            ip_address = request.remote_addr
            user_agent = request.user_agent.string
            
            # Call service to create user
            success, result = self.user_service.create_user_with_roles(
                username=username,
                email=email,
                password=password,
                phone_number=phone_number,
                date_of_birth=date_of_birth,
                gender=gender,
                role_ids=role_ids,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            if not success:
                return jsonify({
                    "status": "error",
                    "message": result
                }), 400
            
            return jsonify({
                "status": "success",
                "message": "Tạo người dùng thành công. Vui lòng kiểm tra email để xác nhận tài khoản.",
                "data": result
            }), 201
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def get_all_roles(self):
        """
        API: GET /api/v1/auth/roles
        Lấy danh sách tất cả roles
        
        Returns:
        {
            "status": "success",
            "data": [
                {"RoleID": 1, "RoleName": "SUPER_ADMIN", "Description": "..."},
                {"RoleID": 2, "RoleName": "HR_MANAGER", "Description": "..."}
            ]
        }
        """
        try:
            roles = self.user_service.get_all_roles()
            return jsonify({
                "status": "success",
                "data": roles
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def verify_email(self):
        """
        API: GET /api/v1/auth/verify-email?token=abc123
        Xác nhận email bằng token
        
        Returns:
        {
            "status": "success",
            "message": "Email đã được xác nhận. Bạn có thể đăng nhập ngay bây giờ."
        }
        """
        try:
            token = request.args.get('token')
            
            if not token:
                return jsonify({
                    "status": "error",
                    "message": "Thiếu token xác nhận"
                }), 400
            
            success, message = self.user_service.verify_email(token)
            
            if not success:
                return jsonify({
                    "status": "error",
                    "message": message
                }), 400
            
            return jsonify({
                "status": "success",
                "message": message
            }), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
    
    def resend_verification_email(self):
        """
        API: POST /api/v1/auth/resend-verification
        Gửi lại email xác nhận
        
        Body:
        {
            "email": "john@example.com"
        }
        """
        try:
            data = request.get_json()
            email = data.get('email')
            
            if not email:
                return jsonify({
                    "status": "error",
                    "message": "Thiếu email"
                }), 400
            
            success, message, token = self.user_service.resend_verification_email(email)
            
            if not success:
                return jsonify({
                    "status": "error",
                    "message": message
                }), 400
            
            return jsonify({
                "status": "success",
                "message": message,
                "data": {
                    "verification_token": token
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi server: {str(e)}"
            }), 500
