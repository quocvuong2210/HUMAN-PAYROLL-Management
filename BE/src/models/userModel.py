from sqlalchemy import create_engine, text
import bcrypt
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
        # Hash password với bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Kiểm tra username và email đã tồn tại chưa
        check_sql = """
            SELECT COUNT(*) as Count FROM [USER] 
            WHERE Username = :username OR Email = :email
        """
        check_result = self._execute(check_sql, {"username": username, "email": email}, fetch=True)
        
        if check_result[0]['Count'] > 0:
            return False, "Username hoặc Email đã tồn tại"
        
        sql = """
            INSERT INTO [USER] (Username, [PasswordHash], Email, PhoneNumber, DateOfBirth, Gender, [Status])
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
        sql = "SELECT UserID, [PasswordHash], [Status] FROM [USER] WHERE Username = :username"
        result = self._execute(sql, {"username": username}, fetch=True)
        
        if not result:
            return False, "Tài khoản không tồn tại"
        
        user = result[0]
        
        # 2. Kiểm tra trạng thái
        if user['Status'] != 'ACTIVE':
            return False, "Tài khoản của bạn đã bị khóa"
        
        # 3. Kiểm tra mật khẩu
        try:
            # Bcrypt check
            if bcrypt.checkpw(password.encode('utf-8'), user['PasswordHash'].encode('utf-8')):
                # Ghi log thành công
                self._log_access(user['UserID'], "LOGIN_SUCCESS", ip_address, user_agent)
                return True, user['UserID']
            else:
                # Ghi log thất bại
                self._log_access(user['UserID'], "LOGIN_FAILED", ip_address, user_agent)
                return False, "Mật khẩu không đúng"
        except Exception as e:
            print(f"Password check error: {e}")
            return False, "Lỗi xác thực mật khẩu"

    def _log_access(self, user_id, action, ip, user_agent):
        """Ghi lại hành động vào bảng ACCESS_LOG"""
        sql = """
            INSERT INTO [ACCESS_LOG] (UserID, Action, IPAddress, UserAgent)
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
            FROM [ACCESS_LOG] 
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
                L.LogID AS LogID, L.UserID, U.Username, U.Email, 
                L.Action, L.IPAddress, L.UserAgent, L.AccessTime
            FROM [ACCESS_LOG] L
            INNER JOIN [USER] U ON L.UserID = U.UserID
            ORDER BY L.AccessTime DESC
        """
        return self._execute(sql, fetch=True)
    def update_user(self, user_id, username=None, email=None, phone=None, dob=None, gender=None, status=None):
        """Cập nhật thông tin người dùng"""
        # Build dynamic SQL chỉ update các field không None
        updates = []
        params = {"user_id": user_id}
        
        if username is not None:
            updates.append("Username = :username")
            params["username"] = username
        
        if email is not None:
            updates.append("Email = :email")
            params["email"] = email
        
        if phone is not None:
            updates.append("PhoneNumber = :phone")
            params["phone"] = phone
        
        if dob is not None:
            updates.append("DateOfBirth = :dob")
            params["dob"] = dob
        
        if gender is not None:
            updates.append("Gender = :gender")
            params["gender"] = gender
        
        if status is not None:
            updates.append("[Status] = :status")
            params["status"] = status
        
        if not updates:
            return True, "Không có gì để cập nhật"
        
        sql = f"""
            UPDATE [USER] 
            SET {', '.join(updates)}
            WHERE UserID = :user_id
        """
        
        try:
            self._execute(sql, params)
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
        sql_get_pwd = "SELECT [PasswordHash] FROM [USER] WHERE UserID = :user_id"
        result = self._execute(sql_get_pwd, {"user_id": user_id}, fetch=True)
        
        if not result:
            return False, "Người dùng không tồn tại"
        
        current_hashed_password = result[0]['PasswordHash']
        
        # 2. Kiểm tra mật khẩu cũ có đúng không (dùng bcrypt)
        try:
            if not bcrypt.checkpw(old_password.encode('utf-8'), current_hashed_password.encode('utf-8')):
                return False, "Mật khẩu cũ không chính xác"
        except Exception as e:
            print(f"Password check error: {e}")
            return False, "Lỗi xác thực mật khẩu cũ"
        
        # 3. Hash mật khẩu mới với bcrypt
        new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        sql_update = "UPDATE [USER] SET [PasswordHash] = :new_password WHERE UserID = :user_id"
        
        try:
            self._execute(sql_update, {
                "new_password": new_hashed_password,
                "user_id": user_id
            })
            return True, "Đổi mật khẩu thành công"
        except Exception as e:
            return False, f"Lỗi cập nhật mật khẩu: {str(e)}"