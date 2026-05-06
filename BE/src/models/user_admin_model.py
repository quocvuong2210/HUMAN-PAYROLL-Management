"""
User Admin Model - Database operations cho admin
"""
from sqlalchemy import create_engine, text
from config import SQL_SERVER_PERMISSION_CONN

class UserAdminModel:
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
    
    def get_all_users_with_roles(self):
        """
        Lấy tất cả users kèm roles
        
        Returns:
            list: Danh sách users với roles
        """
        sql = """
            SELECT 
                U.UserID,
                U.Username,
                U.Email,
                U.PhoneNumber,
                U.DateOfBirth,
                U.Gender,
                U.Status,
                U.EmailVerified,
                U.CreatedAt,
                U.LastLoginAt,
                -- Get roles as comma-separated string
                STUFF((
                    SELECT ',' + R.RoleName
                    FROM [USER_ROLE] UR
                    INNER JOIN [ROLE] R ON UR.RoleID = R.RoleID
                    WHERE UR.UserID = U.UserID
                    FOR XML PATH('')
                ), 1, 1, '') AS Roles,
                -- Get role IDs as comma-separated string
                STUFF((
                    SELECT ',' + CAST(R.RoleID AS NVARCHAR)
                    FROM [USER_ROLE] UR
                    INNER JOIN [ROLE] R ON UR.RoleID = R.RoleID
                    WHERE UR.UserID = U.UserID
                    FOR XML PATH('')
                ), 1, 1, '') AS RoleIDs
            FROM [USER] U
            ORDER BY U.CreatedAt DESC
        """
        
        users = self._execute(sql, fetch=True)
        
        # Parse roles and roleIDs into arrays
        for user in users:
            if user['Roles']:
                user['Roles'] = user['Roles'].split(',')
            else:
                user['Roles'] = []
            
            if user['RoleIDs']:
                user['RoleIDs'] = [int(rid) for rid in user['RoleIDs'].split(',')]
            else:
                user['RoleIDs'] = []
        
        return users
    
    def get_all_access_logs(self):
        """
        Lấy tất cả lịch sử truy cập với thông tin user
        
        Returns:
            list: Danh sách access logs
        """
        sql = """
            SELECT 
                UAL.LogID,
                UAL.UserID,
                UAL.Action,
                UAL.IPAddress,
                UAL.UserAgent,
                UAL.AccessTime,
                U.Username,
                U.Email,
                -- Get user roles
                STUFF((
                    SELECT ',' + R.RoleName
                    FROM [USER_ROLE] UR
                    INNER JOIN [ROLE] R ON UR.RoleID = R.RoleID
                    WHERE UR.UserID = U.UserID
                    FOR XML PATH('')
                ), 1, 1, '') AS UserRoles
            FROM [ACCESS_LOG] UAL
            INNER JOIN [USER] U ON UAL.UserID = U.UserID
            ORDER BY UAL.AccessTime DESC
        """
        
        logs = self._execute(sql, fetch=True)
        
        # Parse roles into array
        for log in logs:
            if log['UserRoles']:
                log['UserRoles'] = log['UserRoles'].split(',')
            else:
                log['UserRoles'] = []
        
        return logs
