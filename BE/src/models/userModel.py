from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash, check_password_hash
from config import SQL_SERVER_PERMISSION_CONN

class UserModel:
    def __init__(self):
        self.engine = create_engine(SQL_SERVER_PERMISSION_CONN)

    def _execute(self, sql, params=None, fetch=False):
        """Hàm thực thi truy vấn nội bộ"""
        with self.engine.connect() as conn:
            with conn.begin():
                query = text(sql)
                result = conn.execute(query, params or {})
                if fetch:
                    return [dict(row._mapping) for row in result.fetchall()]
                return result

    def register(self, username, password, email, phone=None, dob=None, gender=None):
        """Đăng ký user mới với mật khẩu được hash"""
        # Hash password với method='pbkdf2:sha256'
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Kiểm tra username và email đã tồn tại chưa
        check_sql = """
            SELECT COUNT(*) as Count FROM [USER] 
            WHERE Username = :username OR Email = :email
        """
        check_result = self._execute(check_sql, {"username": username, "email": email}, fetch=True)
        
        if check_result[0]['Count'] > 0:
            return False, "Username hoặc Email đã tồn tại"
        
        sql = """
            INSERT INTO [USER] (Username, [Password], Email, PhoneNumber, DateOfBirth, Gender, [Status])
            VALUES (:username, :password, :email, :phone, :dob, :gender, 'ACTIVE')
        """
        try:
            self._execute(sql, {
                "username": username, 
                "password": hashed_password, 
                "email": email, 
                "phone": phone, 
                "dob": dob, 
                "gender": gender
            })
            return True, "Đăng ký thành công"
        except Exception as e:
            return False, f"Lỗi đăng ký: {str(e)}"

    def login(self, username, password, ip_address, user_agent):
        """
        Đăng nhập và ghi log truy cập.
        Trả về (True, UserID) nếu thành công, (False, Thông báo lỗi) nếu thất bại.
        """
        # 1. Lấy thông tin user
        sql = "SELECT UserID, [Password], [Status] FROM [USER] WHERE Username = :username"
        result = self._execute(sql, {"username": username}, fetch=True)
        
        if not result:
            return False, "Tài khoản không tồn tại"
        
        user = result[0]
        
        # 2. Kiểm tra trạng thái
        if user['Status'] != 'ACTIVE':
            return False, "Tài khoản của bạn đã bị khóa"
        
        # 3. Kiểm tra mật khẩu
        if check_password_hash(user['Password'], password):
            # Ghi log thành công
            self._log_access(user['UserID'], "LOGIN_SUCCESS", ip_address, user_agent)
            return True, user['UserID']
        else:
            # Ghi log thất bại
            self._log_access(user['UserID'], "LOGIN_FAILED", ip_address, user_agent)
            return False, "Mật khẩu không đúng"

    def _log_access(self, user_id, action, ip, user_agent):
        """Ghi lại hành động vào bảng UserAccessLog"""
        sql = """
            INSERT INTO [UserAccessLog] (UserID, Action, IPAddress, UserAgent)
            VALUES (:uid, :action, :ip, :ua)
        """
        self._execute(sql, {"uid": user_id, "action": action, "ip": ip, "ua": user_agent})
    def get_user_full_profile(self, user_id):
        """Lấy profile chi tiết và toàn bộ lịch sử truy cập của user"""
        # 1. Lấy thông tin user
        sql_user = """
            SELECT UserID, Username, Email, PhoneNumber, DateOfBirth, Gender, Status, CreatedAt 
            FROM [USER] WHERE UserID = :user_id
        """
        user_result = self._execute(sql_user, {"user_id": user_id}, fetch=True)
        
        if not user_result:
            return {"status": "error", "message": "Không tìm thấy người dùng"}
        
        # 2. Lấy lịch sử truy cập (sắp xếp theo thời gian mới nhất)
        sql_logs = """
            SELECT Action, IPAddress, UserAgent, AccessTime 
            FROM [UserAccessLog] 
            WHERE UserID = :user_id 
            ORDER BY AccessTime DESC
        """
        logs_result = self._execute(sql_logs, {"user_id": user_id}, fetch=True)
        
        # 3. Kết hợp dữ liệu
        user_data = user_result[0]
        user_data['access_history'] = logs_result # Thêm danh sách log vào object user
        
        return {"status": "success", "data": user_data}
    def get_user_by_id(self, user_id):
        """Lấy thông tin cơ bản của user dựa trên UserID"""
        sql = """
            SELECT UserID, Username, Email, PhoneNumber, DateOfBirth, Gender, Status, CreatedAt 
            FROM [USER] 
            WHERE UserID = :user_id
        """
        result = self._execute(sql, {"user_id": user_id}, fetch=True)
        
        if result:
            return {"status": "success", "data": result[0]}
        return {"status": "error", "message": "Không tìm thấy user với ID này"}
    def get_all_users(self):
        """Lấy danh sách tất cả người dùng trong hệ thống"""
        sql = "SELECT UserID, Username, Email, PhoneNumber, DateOfBirth, Gender, Status, CreatedAt FROM [USER]"
        return self._execute(sql, fetch=True)

    def get_all_access_logs(self):
        """
        Lấy toàn bộ lịch sử truy cập của tất cả người dùng.
        Kết hợp JOIN với bảng USER để lấy thông tin cá nhân của người truy cập.
        """
        sql = """
            SELECT 
                L.Id AS LogID, L.UserID, U.Username, U.Email, 
                L.Action, L.IPAddress, L.UserAgent, L.AccessTime
            FROM [UserAccessLog] L
            INNER JOIN [USER] U ON L.UserID = U.UserID
            ORDER BY L.AccessTime DESC
        """
        return self._execute(sql, fetch=True)
    def update_user(self, user_id, username=None, email=None, phone=None, dob=None, gender=None, status=None):
        """Cập nhật thông tin người dùng"""
        sql = """
            UPDATE [USER] 
            SET Username = ISNULL(:username, Username),
                Email = ISNULL(:email, Email),
                PhoneNumber = ISNULL(:phone, PhoneNumber),
                DateOfBirth = ISNULL(:dob, DateOfBirth),
                Gender = ISNULL(:gender, Gender),
                [Status] = ISNULL(:status, [Status])
            WHERE UserID = :user_id
        """
        try:
            self._execute(sql, {
                "user_id": user_id,
                "username": username,
                "email": email,
                "phone": phone,
                "dob": dob,
                "gender": gender,
                "status": status
            })
            return True, "Cập nhật thành công"
        except Exception as e:
            return False, f"Lỗi cập nhật: {str(e)}"

    def delete_user(self, user_id):
        """Xóa người dùng (Dữ liệu log liên quan sẽ tự động xóa nhờ ON DELETE CASCADE)"""
        sql = "DELETE FROM [USER] WHERE UserID = :user_id"
        try:
            self._execute(sql, {"user_id": user_id})
            return True, "Xóa người dùng thành công"
        except Exception as e:
            return False, f"Lỗi xóa: {str(e)}"
    def change_password(self, user_id, old_password, new_password):
        """
        Thay đổi mật khẩu sau khi xác thực mật khẩu cũ.
        """
        # 1. Lấy mật khẩu cũ hiện tại từ database
        sql_get_pwd = "SELECT [Password] FROM [USER] WHERE UserID = :user_id"
        result = self._execute(sql_get_pwd, {"user_id": user_id}, fetch=True)
        
        if not result:
            return False, "Người dùng không tồn tại"
        
        current_hashed_password = result[0]['Password']
        
        # 2. Kiểm tra mật khẩu cũ có đúng không
        if not check_password_hash(current_hashed_password, old_password):
            return False, "Mật khẩu cũ không chính xác"
        
        # 3. Hash mật khẩu mới và update với method='pbkdf2:sha256'
        new_hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
        sql_update = "UPDATE [USER] SET [Password] = :new_password WHERE UserID = :user_id"
        
        try:
            self._execute(sql_update, {
                "new_password": new_hashed_password,
                "user_id": user_id
            })
            return True, "Đổi mật khẩu thành công"
        except Exception as e:
            return False, f"Lỗi cập nhật mật khẩu: {str(e)}"