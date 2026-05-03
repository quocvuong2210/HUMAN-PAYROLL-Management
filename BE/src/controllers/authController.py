from flask import jsonify, request
from src.services.auth_service import AuthService

class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    # ================= ĐĂNG KÝ (REGISTER) =================
    def register(self):
        """API Đăng ký người dùng mới"""
        try:
            data = request.get_json()
            
            # Kiểm tra trường bắt buộc
            required = ['username', 'email', 'password']
            if not data or not all(k in data for k in required):
                return jsonify({"status": "error", "message": "Thiếu thông tin bắt buộc"}), 400
            
            # Gọi service đăng ký
            result = self.auth_service.register(data)
            
            status_code = 201 if result["status"] == "success" else 400
            return jsonify(result), status_code

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    # ================= ĐĂNG NHẬP (LOGIN) =================
    def login(self):
        """API xác thực và cấp Token"""
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return jsonify({"status": "error", "message": "Thiếu tài khoản hoặc mật khẩu"}), 400

            # Service xử lý logic login và ghi log vào UserAccessLog
            result = self.auth_service.login(username, password, request)

            if result["status"] == "success":
                return jsonify(result), 200
            
            return jsonify(result), 401

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    # ================= THÔNG TIN CÁ NHÂN (PROFILE) =================
    def get_profile(self):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"status": "error", "message": "Yêu cầu Token"}), 401

            token = auth_header.split(" ")[1]
            user_id = self.auth_service.verify_token(token) # Lấy ID từ token

            if not user_id:
                return jsonify({"status": "error", "message": "Token không hợp lệ"}), 401

            # Gọi hàm mới để lấy cả Profile + Logs
            profile_data = self.auth_service.get_user_full_profile(user_id)
            return jsonify(profile_data), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    def get_user_info(self, user_id):
        """API lấy thông tin chi tiết của 1 user bất kỳ (Dùng cho Admin hoặc chính chủ)"""
        try:
            # Bạn có thể thêm logic kiểm tra quyền ở đây (ví dụ: chỉ Admin mới được xem ID người khác)
            result = self.auth_service.get_user_by_id(user_id)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    def get_all_users_list(self):
        """API cho Admin lấy danh sách user"""
        try:
            result = self.auth_service.get_all_users()
            return jsonify({"status": "success", "data": result}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    def get_full_system_logs(self):
        """API cho Admin lấy toàn bộ log của hệ thống"""
        try:
            result = self.auth_service.get_all_access_logs()
            return jsonify({"status": "success", "data": result}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    def update_user(self, user_id):
        try:
            data = request.get_json()
            success, message = self.auth_service.update_user(user_id, data)
            return jsonify({"status": "success" if success else "error", "message": message}), 200 if success else 400
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    def delete_user(self, user_id):
        try:
            success, message = self.auth_service.delete_user(user_id)
            return jsonify({"status": "success" if success else "error", "message": message}), 200 if success else 400
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    def change_password(self):
        """
        API Đổi mật khẩu
        """
        try:
            # 1. Lấy Token từ header để xác định user_id
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"status": "error", "message": "Yêu cầu Token"}), 401
            
            token = auth_header.split(" ")[1]
            user_id = self.auth_service.verify_token(token)
            
            if not user_id:
                return jsonify({"status": "error", "message": "Token không hợp lệ"}), 401

            # 2. Lấy thông tin old_password và new_password từ Body
            data = request.get_json()
            
            # 3. Gọi Service xử lý đổi mật khẩu
            result = self.auth_service.change_password(user_id, data)
            
            # 4. Trả về kết quả
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500