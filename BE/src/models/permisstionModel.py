from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN # Giả sử DB Permission nằm cùng server MSSQL

class PermissionModel:
    def __init__(self):
        self.engine = create_engine(SQL_SERVER_PERMISSION_CONN)

    def _execute(self, sql, params=None, fetch=False):
        """Hàm tiện ích thực thi câu lệnh SQL"""
        with self.engine.connect() as conn:
            result = conn.execute(text(sql), params or {})
            if fetch:
                # Trả về list các dict để dễ xử lý ở Controller
                return [dict(row._mapping) for row in result.fetchall()]
            conn.commit()
            return result.rowcount

    def get_user_permissions(self, user_id):
        """Lấy danh sách tất cả các PermissionName của một user cụ thể"""
        query = """
            SELECT DISTINCT P.PermissionName
            FROM [USER_ROLE] UR
            JOIN [ROLE_PERMISSION] RP ON UR.RoleID = RP.RoleID
            JOIN [PERMISSION] P ON RP.PermissionID = P.PermissionID
            WHERE UR.UserID = :user_id
        """
        rows = self._execute(query, {"user_id": user_id}, fetch=True)
        return [row['PermissionName'] for row in rows]

    def check_user_access(self, user_id, function_name):
        """Kiểm tra quyền truy cập Function"""
        query = """
            SELECT 1
            FROM [USER_ROLE] UR
            JOIN [ROLE_PERMISSION] RP ON UR.RoleID = RP.RoleID
            JOIN [PERMISSION_FUNCTION] PF ON RP.PermissionID = PF.PermissionID
            JOIN [SYSTEMFUNCTION] SF ON PF.FunctionID = SF.FunctionID
            WHERE UR.UserID = :user_id AND SF.FunctionName = :func_name
        """
        result = self._execute(query, {"user_id": user_id, "func_name": function_name}, fetch=True)
        return len(result) > 0

    def assign_role_to_user(self, user_id, role_id):
        """Cấp vai trò cho User (Có kiểm tra trùng lặp)"""
        try:
            # Xóa role cũ trước khi gán mới (nếu muốn 1 user 1 role)
            # Hoặc dùng logic kiểm tra tồn tại
            query = "INSERT INTO [USER_ROLE] (UserID, RoleID) VALUES (:user_id, :role_id)"
            self._execute(query, {"user_id": user_id, "role_id": role_id})
            return True, "Cấp vai trò thành công"
        except Exception as e:
            return False, str(e)
    def get_user_permissions(self, user_id):
        """Lấy danh sách tất cả các PermissionName của một user cụ thể"""
        query = """
            SELECT DISTINCT P.PermissionName
            FROM [USER_ROLE] UR
            JOIN [ROLE_PERMISSION] RP ON UR.RoleID = RP.RoleID
            JOIN [PERMISSION] P ON RP.PermissionID = P.PermissionID
            WHERE UR.UserID = :user_id
        """
        rows = self._execute(query, {"user_id": user_id}, fetch=True)
        return [row['PermissionName'] for row in rows]

    def check_user_access(self, user_id, function_name):
        """Kiểm tra quyền truy cập Function"""
        query = """
            SELECT 1
            FROM [USER_ROLE] UR
            JOIN [ROLE_PERMISSION] RP ON UR.RoleID = RP.RoleID
            JOIN [PERMISSION_FUNCTION] PF ON RP.PermissionID = PF.PermissionID
            JOIN [SYSTEMFUNCTION] SF ON PF.FunctionID = SF.FunctionID
            WHERE UR.UserID = :user_id AND SF.FunctionName = :func_name
        """
        result = self._execute(query, {"user_id": user_id, "func_name": function_name}, fetch=True)
        return len(result) > 0

    def assign_role_to_user(self, user_id, role_id):
        """Cấp vai trò cho User (Có kiểm tra trùng lặp)"""
        try:
            # Xóa role cũ trước khi gán mới (nếu muốn 1 user 1 role)
            # Hoặc dùng logic kiểm tra tồn tại
            query = "INSERT INTO [USER_ROLE] (UserID, RoleID) VALUES (:user_id, :role_id)"
            self._execute(query, {"user_id": user_id, "role_id": role_id})
            return True, "Cấp vai trò thành công"
        except Exception as e:
            return False, str(e)