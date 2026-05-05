"""
RBAC Management Service - Business logic cho quản lý RBAC
"""
from src.models.rbacModel import RBACModel

class RBACManagementService:
    def __init__(self):
        self.rbac_model = RBACModel()
    
    # ==================== ROLE PERMISSIONS ====================
    
    def get_role_permissions(self, role_id):
        """
        Lấy danh sách permissions của role
        
        Args:
            role_id: ID của role
            
        Returns:
            dict: Response với danh sách permissions
        """
        permissions = self.rbac_model.get_role_permissions(role_id)
        
        return {
            "status": "success",
            "data": permissions
        }
    
    def update_role_permissions(self, role_id, permission_ids):
        """
        Cập nhật toàn bộ permissions của role
        (Xóa tất cả permissions cũ và gán permissions mới)
        
        Args:
            role_id: ID của role
            permission_ids: List các PermissionID mới
            
        Returns:
            dict: Response với status
        """
        # 1. Lấy permissions hiện tại
        current_permissions = self.rbac_model.get_role_permissions(role_id)
        current_permission_ids = [perm['PermissionID'] for perm in current_permissions]
        
        # 2. Xóa permissions cũ
        for permission_id in current_permission_ids:
            self.rbac_model._execute(
                "DELETE FROM [ROLE_PERMISSION] WHERE RoleID = :role_id AND PermissionID = :perm_id",
                {"role_id": role_id, "perm_id": permission_id}
            )
        
        # 3. Thêm permissions mới
        assigned_permissions = []
        failed_permissions = []
        
        for permission_id in permission_ids:
            try:
                self.rbac_model._execute(
                    "INSERT INTO [ROLE_PERMISSION] (RoleID, PermissionID) VALUES (:role_id, :perm_id)",
                    {"role_id": role_id, "perm_id": permission_id}
                )
                assigned_permissions.append(permission_id)
            except Exception as e:
                failed_permissions.append({"permission_id": permission_id, "error": str(e)})
        
        return {
            "status": "success",
            "message": "Cập nhật permissions thành công",
            "data": {
                "assigned_permissions": assigned_permissions,
                "failed_permissions": failed_permissions
            }
        }
    
    def add_permission_to_role(self, role_id, permission_id):
        """
        Thêm permission cho role
        
        Args:
            role_id: ID của role
            permission_id: ID của permission
            
        Returns:
            dict: Response với status
        """
        try:
            self.rbac_model._execute(
                "INSERT INTO [ROLE_PERMISSION] (RoleID, PermissionID) VALUES (:role_id, :perm_id)",
                {"role_id": role_id, "perm_id": permission_id}
            )
            return {"status": "success", "message": "Thêm permission thành công"}
        except Exception as e:
            return {"status": "error", "message": f"Lỗi: {str(e)}"}
    
    def remove_permission_from_role(self, role_id, permission_id):
        """
        Xóa permission khỏi role
        
        Args:
            role_id: ID của role
            permission_id: ID của permission
            
        Returns:
            dict: Response với status
        """
        try:
            self.rbac_model._execute(
                "DELETE FROM [ROLE_PERMISSION] WHERE RoleID = :role_id AND PermissionID = :perm_id",
                {"role_id": role_id, "perm_id": permission_id}
            )
            return {"status": "success", "message": "Xóa permission thành công"}
        except Exception as e:
            return {"status": "error", "message": f"Lỗi: {str(e)}"}
    
    # ==================== PERMISSION FUNCTIONS ====================
    
    def get_permission_functions(self, permission_id):
        """
        Lấy danh sách functions của permission
        
        Args:
            permission_id: ID của permission
            
        Returns:
            dict: Response với danh sách functions
        """
        functions = self.rbac_model.get_permission_functions(permission_id)
        
        return {
            "status": "success",
            "data": functions
        }
    
    # ==================== ROLE MANAGEMENT ====================
    
    def create_role(self, role_name, description=None):
        """
        Tạo role mới
        
        Args:
            role_name: Tên role
            description: Mô tả role
            
        Returns:
            dict: Response với status
        """
        success, message = self.rbac_model.create_role(role_name, description)
        
        if success:
            return {"status": "success", "message": message}
        
        return {"status": "error", "message": message}
    
    def update_role(self, role_id, data):
        """
        Cập nhật thông tin role
        
        Args:
            role_id: ID của role
            data: dict chứa thông tin cần update
            
        Returns:
            dict: Response với status
        """
        try:
            sql = """
                UPDATE [ROLE]
                SET RoleName = ISNULL(:role_name, RoleName),
                    Description = ISNULL(:description, Description)
                WHERE RoleID = :role_id
            """
            self.rbac_model._execute(sql, {
                "role_id": role_id,
                "role_name": data.get('role_name'),
                "description": data.get('description')
            })
            return {"status": "success", "message": "Cập nhật role thành công"}
        except Exception as e:
            return {"status": "error", "message": f"Lỗi: {str(e)}"}
    
    def delete_role(self, role_id):
        """
        Xóa role
        
        Args:
            role_id: ID của role
            
        Returns:
            dict: Response với status
        """
        try:
            self.rbac_model._execute(
                "DELETE FROM [ROLE] WHERE RoleID = :role_id",
                {"role_id": role_id}
            )
            return {"status": "success", "message": "Xóa role thành công"}
        except Exception as e:
            return {"status": "error", "message": f"Lỗi: {str(e)}"}
    
    # ==================== STATISTICS ====================
    
    def get_statistics(self):
        """
        Lấy thống kê RBAC
        
        Returns:
            dict: Response với thống kê
        """
        # Đếm số roles
        roles_count = len(self.rbac_model.get_all_roles())
        
        # Đếm số permissions
        permissions_count = len(self.rbac_model.get_all_permissions())
        
        # Đếm số functions
        functions_count = len(self.rbac_model.get_all_functions())
        
        # Đếm số user-role assignments
        user_roles_count = self.rbac_model._execute(
            "SELECT COUNT(*) as Count FROM [USER_ROLE]",
            fetch=True
        )[0]['Count']
        
        # Đếm số role-permission assignments
        role_permissions_count = self.rbac_model._execute(
            "SELECT COUNT(*) as Count FROM [ROLE_PERMISSION]",
            fetch=True
        )[0]['Count']
        
        return {
            "status": "success",
            "data": {
                "total_roles": roles_count,
                "total_permissions": permissions_count,
                "total_functions": functions_count,
                "total_user_role_assignments": user_roles_count,
                "total_role_permission_assignments": role_permissions_count
            }
        }
