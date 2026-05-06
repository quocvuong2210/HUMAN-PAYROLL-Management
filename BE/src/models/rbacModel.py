"""
RBAC Model - Quản lý Role-Based Access Control
"""
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

class RBACModel:
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
    
    # ==================== ROLE MANAGEMENT ====================
    
    def get_all_roles(self):
        """Lấy danh sách tất cả các role"""
        sql = "SELECT RoleID, RoleName, Description FROM [ROLE]"
        return self._execute(sql, fetch=True)
    
    def get_role_by_id(self, role_id):
        """Lấy thông tin role theo ID"""
        sql = "SELECT RoleID, RoleName, Description FROM [ROLE] WHERE RoleID = :role_id"
        result = self._execute(sql, {"role_id": role_id}, fetch=True)
        return result[0] if result else None
    
    def create_role(self, role_name, description=None):
        """Tạo role mới"""
        sql = """
            INSERT INTO [ROLE] (RoleName, Description)
            VALUES (:role_name, :description)
        """
        try:
            self._execute(sql, {"role_name": role_name, "description": description})
            return True, "Tạo role thành công"
        except Exception as e:
            return False, f"Lỗi tạo role: {str(e)}"
    
    # ==================== USER ROLE ASSIGNMENT ====================
    
    def assign_role_to_user(self, user_id, role_id):
        """Gán role cho user"""
        sql = """
            INSERT INTO [USER_ROLE] (UserID, RoleID)
            VALUES (:user_id, :role_id)
        """
        try:
            self._execute(sql, {"user_id": user_id, "role_id": role_id})
            return True, "Gán role thành công"
        except Exception as e:
            return False, f"Lỗi gán role: {str(e)}"
    
    def remove_role_from_user(self, user_id, role_id):
        """Xóa role khỏi user"""
        sql = """
            DELETE FROM [USER_ROLE]
            WHERE UserID = :user_id AND RoleID = :role_id
        """
        try:
            self._execute(sql, {"user_id": user_id, "role_id": role_id})
            return True, "Xóa role thành công"
        except Exception as e:
            return False, f"Lỗi xóa role: {str(e)}"
    
    def get_user_roles(self, user_id):
        """Lấy danh sách role của user"""
        sql = """
            SELECT R.RoleID, R.RoleName, R.Description
            FROM [USER_ROLE] UR
            INNER JOIN [ROLE] R ON UR.RoleID = R.RoleID
            WHERE UR.UserID = :user_id
        """
        return self._execute(sql, {"user_id": user_id}, fetch=True)
    
    # ==================== PERMISSION MANAGEMENT ====================
    
    def get_all_permissions(self):
        """Lấy danh sách tất cả permissions"""
        sql = "SELECT PermissionID, PermissionName, Description FROM [PERMISSION]"
        return self._execute(sql, fetch=True)
    
    def get_role_permissions(self, role_id):
        """Lấy danh sách permission của role"""
        sql = """
            SELECT P.PermissionID, P.PermissionName, P.Description
            FROM [ROLE_PERMISSION] RP
            INNER JOIN [PERMISSION] P ON RP.PermissionID = P.PermissionID
            WHERE RP.RoleID = :role_id
        """
        return self._execute(sql, {"role_id": role_id}, fetch=True)
    
    # ==================== FUNCTION MANAGEMENT ====================
    
    def get_all_functions(self):
        """Lấy danh sách tất cả system functions"""
        sql = "SELECT FunctionID, FunctionName, Description FROM [SYSTEMFUNCTION]"
        return self._execute(sql, fetch=True)
    
    def get_permission_functions(self, permission_id):
        """Lấy danh sách function của permission"""
        sql = """
            SELECT SF.FunctionID, SF.FunctionName, SF.Description
            FROM [PERMISSION_FUNCTION] PF
            INNER JOIN [SYSTEMFUNCTION] SF ON PF.FunctionID = SF.FunctionID
            WHERE PF.PermissionID = :permission_id
        """
        return self._execute(sql, {"permission_id": permission_id}, fetch=True)
    
    # ==================== USER PERMISSIONS CHECK ====================
    
    def get_user_permissions(self, user_id):
        """
        Lấy tất cả các function mà user có quyền thực hiện
        Thông qua chuỗi: User -> Role -> Permission -> Function
        
        Returns:
            list: Danh sách FunctionName
        """
        sql = """
            SELECT DISTINCT SF.FunctionName
            FROM [USER] U
            INNER JOIN [USER_ROLE] UR ON U.UserID = UR.UserID
            INNER JOIN [ROLE_PERMISSION] RP ON UR.RoleID = RP.RoleID
            INNER JOIN [PERMISSION_FUNCTION] PF ON RP.PermissionID = PF.PermissionID
            INNER JOIN [SYSTEMFUNCTION] SF ON PF.FunctionID = SF.FunctionID
            WHERE U.UserID = :user_id
        """
        result = self._execute(sql, {"user_id": user_id}, fetch=True)
        return [row['FunctionName'] for row in result]
    
    def check_user_permission(self, user_id, function_name):
        """
        Kiểm tra user có quyền thực hiện function cụ thể không
        
        Args:
            user_id: ID người dùng
            function_name: Tên function cần kiểm tra (VD: 'USER_EDIT')
            
        Returns:
            bool: True nếu có quyền, False nếu không
        """
        sql = """
            SELECT COUNT(*) AS HasPermission
            FROM [USER] U
            INNER JOIN [USER_ROLE] UR ON U.UserID = UR.UserID
            INNER JOIN [ROLE_PERMISSION] RP ON UR.RoleID = RP.RoleID
            INNER JOIN [PERMISSION_FUNCTION] PF ON RP.PermissionID = PF.PermissionID
            INNER JOIN [SYSTEMFUNCTION] SF ON PF.FunctionID = SF.FunctionID
            WHERE U.UserID = :user_id AND SF.FunctionName = :function_name
        """
        result = self._execute(sql, {"user_id": user_id, "function_name": function_name}, fetch=True)
        return result[0]['HasPermission'] > 0 if result else False
    
    # ==================== USER FULL PERMISSIONS INFO ====================
    
    def get_user_full_permissions(self, user_id):
        """
        Lấy thông tin đầy đủ về quyền của user
        Bao gồm: Roles, Permissions, Functions
        
        Returns:
            dict: {
                "roles": [...],
                "permissions": [...],
                "functions": [...]  # List of function names (strings)
            }
        """
        # 1. Lấy roles
        roles = self.get_user_roles(user_id)
        
        # 2. Lấy permissions (từ tất cả roles)
        sql_permissions = """
            SELECT DISTINCT P.PermissionID, P.PermissionName, P.Description
            FROM [USER_ROLE] UR
            INNER JOIN [ROLE_PERMISSION] RP ON UR.RoleID = RP.RoleID
            INNER JOIN [PERMISSION] P ON RP.PermissionID = P.PermissionID
            WHERE UR.UserID = :user_id
        """
        permissions = self._execute(sql_permissions, {"user_id": user_id}, fetch=True)
        
        # 3. Lấy functions (already returns list of strings)
        functions = self.get_user_permissions(user_id)
        
        return {
            "roles": roles,
            "permissions": permissions,
            "functions": functions  # List of function names
        }

