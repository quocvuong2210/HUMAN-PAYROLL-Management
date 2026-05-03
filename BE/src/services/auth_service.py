import jwt
import datetime
from src.models.userModel import UserModel # Trỏ tới model bạn đã viết
from werkzeug.security import generate_password_hash
from src.utils.inspector import UserInspector

class AuthService:
    def __init__(self):
        self.model = UserModel() # Khởi tạo model User của bạn
        self.inspector = UserInspector()
        self.secret_key = "YOUR_SECRET_KEY" # Lấy từ file config

    # --- 1. AUTHENTICATION ---
    def register(self, data):
        """Đăng ký user với mật khẩu đã hash"""
        # Lưu ý: UserModel của bạn trong ví dụ trên đã tự hash, 
        # nhưng nếu bạn muốn kiểm soát ở Service thì có thể hash ở đây.
        success, message = self.model.register(
            username=data.get('username'),
            password=data.get('password'), # UserModel sẽ tự hash
            email=data.get('email'),
            phone=data.get('phone'),
            dob=data.get('dob'),
            gender=data.get('gender')
        )
        
        if not success:
            return {"status": "error", "message": message}
        return {"status": "success", "message": "Đăng ký thành công"}

    def login(self, username, password, request):
        """Xử lý đăng nhập và tạo JWT token"""
        ip = self.inspector.get_client_ip(request)
        ua = request.user_agent.string
        
        # Gọi model để xác thực và ghi log
        is_authenticated, result = self.model.login(username, password, ip, ua)
        
        if not is_authenticated:
            return {"status": "error", "message": result} # result lúc này là thông báo lỗi
        
        # Nếu thành công, result chính là user_id
        token = jwt.encode({
            "user_id": result,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        }, self.secret_key, algorithm="HS256")
        
        return {
            "status": "success", 
            "token": token, 
            "user_id": result
        }
    # --- 2. TOKEN & PROFILE MANAGEMENT ---
    def verify_token(self, token):
        """Giải mã và kiểm tra tính hợp lệ của token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload.get("user_id")
        except jwt.ExpiredSignatureError:
            return None # Token hết hạn
        except jwt.InvalidTokenError:
            return None # Token không hợp lệ

    def get_user_full_profile(self, user_id):
        """Lấy thông tin cá nhân kèm lịch sử truy cập"""
        return self.model.get_user_full_profile(user_id)
    def get_user_by_id(self, user_id):
        """Service gọi model lấy thông tin user theo ID"""
        return self.model.get_user_by_id(user_id)
    def get_all_users(self):
        return self.model.get_all_users()

    def get_all_access_logs(self):
        return self.model.get_all_access_logs()
    def update_user(self, user_id, data):
        return self.model.update_user(
            user_id, 
            data.get('username'), 
            data.get('email'), 
            data.get('phone'), 
            data.get('dob'), 
            data.get('gender'),
            data.get('status')
        )

    def delete_user(self, user_id):
        return self.model.delete_user(user_id)
    def change_password(self, user_id, data):
        """
        Service xử lý đổi mật khẩu:
        data gồm: old_password, new_password
        """
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return {"status": "error", "message": "Thiếu thông tin mật khẩu"}
            
        success, message = self.model.change_password(user_id, old_password, new_password)
        
        if success:
            return {"status": "success", "message": message}
        return {"status": "error", "message": message}