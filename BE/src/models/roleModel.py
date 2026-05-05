"""
Role Model - Quản lý vai trò và phân quyền
"""
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

class RoleModel:
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
    
    def get_all_roles(self):
        """Lấy danh sách tất cả roles"""
        sql = "SELECT RoleID, RoleName, Description FROM [ROLE] ORDER BY RoleID"
        return self._execute(sql, fetch=True)
    
    def get_user_roles(self, user_id):
        """Lấy danh sách roles của user"""
        sql = """
            SELECT R.RoleID, R.RoleName
            FROM [USER_ROLE] UR
            INNER JOIN [ROLE] R ON UR.RoleID = R.RoleID
            WHERE UR.UserID = :user_id
            ORDER BY R.RoleID
        """
        return self._execute(sql, {"user_id": user_id}, fetch=True)
    
    def update_user_roles(self, user_id, role_ids):
        """
        Cập nhật roles của user
        - Xóa tất cả roles cũ
        - Thêm roles mới
        """
        try:
            # 1. Xóa tất cả roles cũ
            delete_sql = "DELETE FROM [USER_ROLE] WHERE UserID = :user_id"
            self._execute(delete_sql, {"user_id": user_id})
            
            # 2. Thêm roles mới
            if role_ids:
                for role_id in role_ids:
                    insert_sql = """
                        INSERT INTO [USER_ROLE] (UserID, RoleID)
                        VALUES (:user_id, :role_id)
                    """
                    self._execute(insert_sql, {
                        "user_id": user_id,
                        "role_id": role_id
                    })
            
            return True, "Cập nhật vai trò thành công"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"
    
    def get_role_permissions(self, role_id):
        """Lấy danh sách permissions của role"""
        sql = """
            SELECT P.PermissionID, P.PermissionName
            FROM [ROLE_PERMISSION] RP
            INNER JOIN [PERMISSION] P ON RP.PermissionID = P.PermissionID
            WHERE RP.RoleID = :role_id
            ORDER BY P.PermissionID
        """
        return self._execute(sql, {"role_id": role_id}, fetch=True)
    
    def get_user_permissions(self, user_id):
        """Lấy tất cả permissions của user thông qua roles"""
        sql = """
            SELECT DISTINCT P.PermissionID, P.PermissionName
            FROM [USER_ROLE] UR
            INNER JOIN [ROLE_PERMISSION] RP ON UR.RoleID = RP.RoleID
            INNER JOIN [PERMISSION] P ON RP.PermissionID = P.PermissionID
            WHERE UR.UserID = :user_id
            ORDER BY P.PermissionID
        """
        return self._execute(sql, {"user_id": user_id}, fetch=True)
    
    def get_user_functions(self, user_id):
        """Lấy tất cả functions của user"""
        sql = """
            SELECT DISTINCT SF.FunctionID, SF.FunctionName
            FROM [USER_ROLE] UR
            INNER JOIN [ROLE_PERMISSION] RP ON UR.RoleID = RP.RoleID
            INNER JOIN [PERMISSION_FUNCTION] PF ON RP.PermissionID = PF.PermissionID
            INNER JOIN [SYSTEMFUNCTION] SF ON PF.FunctionID = SF.FunctionID
            WHERE UR.UserID = :user_id
            ORDER BY SF.FunctionID
        """
        return self._execute(sql, {"user_id": user_id}, fetch=True)
    
    def check_user_permission(self, user_id, function_name):
        """Kiểm tra user có quyền thực hiện function không"""
        sql = """
            SELECT COUNT(*) AS HasPermission
            FROM [USER_ROLE] UR
            INNER JOIN [ROLE_PERMISSION] RP ON UR.RoleID = RP.RoleID
            INNER JOIN [PERMISSION_FUNCTION] PF ON RP.PermissionID = PF.PermissionID
            INNER JOIN [SYSTEMFUNCTION] SF ON PF.FunctionID = SF.FunctionID
            WHERE UR.UserID = :user_id AND SF.FunctionName = :function_name
        """
        result = self._execute(sql, {
            "user_id": user_id,
            "function_name": function_name
        }, fetch=True)
        
        return result[0]['HasPermission'] > 0 if result else False
