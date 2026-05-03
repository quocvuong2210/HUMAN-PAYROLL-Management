import re
from datetime import datetime
from src.models.employee_model import EmployeeModel

class EmployeeService:
    def __init__(self):
        self.model = EmployeeModel()

    # --- 1. LẤY DANH SÁCH NHÂN VIÊN ---
    def list_employees(self, filters):
        try:
            page = int(filters.get('page', 1))
            limit = int(filters.get('limit', 10))
            
            # Xử lý ID sang kiểu int để tránh lỗi SQL
            def to_int(val):
                return int(val) if val and str(val).isdigit() else None

            return self.model.get_employees_paged(
                page=page, 
                limit=limit, 
                name=filters.get('name'), 
                dept_id=to_int(filters.get('dept_id')), 
                pos_id=to_int(filters.get('pos_id')),
                status=filters.get('status'),
                gender=filters.get('gender'),
                start_date=filters.get('start_date'),
                end_date=filters.get('end_date')
            )
        except Exception as e:
            print(f"Service Error (List): {e}")
            raise e

    # --- 2. THÊM MỚI NHÂN VIÊN ---
    def create_employee(self, data):
        try:
            # A. Kiểm tra định dạng và các trường bắt buộc
            self._validate_basic_info(data, is_update=False)

            # B. Kiểm tra nghiệp vụ sâu (Database Check)
            self._check_business_constraints(data)

            # C. Thực hiện lưu
            new_id = self.model.create_employee(data)
            
            return {
                "status": "success", 
                "message": f"Nhân viên {data['FullName']} đã được tạo và đồng bộ.", 
                "id": new_id
            }
        except ValueError as ve:
            return {"status": "error", "message": str(ve)}
        except Exception as e:
            print(f"Service Error (Create): {e}")
            return {"status": "error", "message": f"Lỗi hệ thống: {str(e)}"}

    # --- 3. CẬP NHẬT NHÂN VIÊN ---
    def update_employee(self, emp_id, data):
        try:
            if not emp_id:
                raise ValueError("Thiếu ID nhân viên.")

            # A. Kiểm tra xem nhân viên có tồn tại không
            current_emp = self.model.get_full_employee_info(emp_id)
            if not current_emp:
                return {"status": "error", "message": "Không tìm thấy nhân viên để cập nhật."}

            # B. Validate dữ liệu đầu vào
            self._validate_basic_info(data, is_update=True)
            self._check_business_constraints(data, is_update=True, emp_id=emp_id)

            # C. Cập nhật
            self.model.update_employee(emp_id, data)
            return {"status": "success", "message": "Cập nhật dữ liệu thành công."}
        except ValueError as ve:
            return {"status": "error", "message": str(ve)}
        except Exception as e:
            print(f"Service Error (Update): {e}")
            return {"status": "error", "message": "Lỗi hệ thống khi cập nhật."}

    # --- 4. XÓA NHÂN VIÊN ---
    def delete_employee(self, emp_id):
        try:
            # Kiểm tra tồn tại trước khi xóa để có thông báo rõ ràng
            check_emp = self.model.get_full_employee_info(emp_id)
            if not check_emp:
                return {"status": "error", "message": "Nhân viên không tồn tại hoặc đã bị xóa."}

            self.model.delete_employee_complete(emp_id)
            return {"status": "success", "message": f"Đã xóa toàn bộ hồ sơ của nhân viên: {check_emp['FullName']}"}
        except Exception as e:
            print(f"Service Error (Delete): {e}")
            return {"status": "error", "message": "Không thể xóa do ràng buộc dữ liệu liên quan."}

    # --- HÀM KIỂM TRA RÀNG BUỘC NGHIỆP VỤ (CHỐT CHẶN CUỐI) ---
    def _check_business_constraints(self, data, is_update=False, emp_id=None):
        """Kiểm tra sự tồn tại của FK và trùng lặp Email/SĐT trong DB"""
        errors = []

        # 1. Kiểm tra Phòng ban (DepartmentID)
        if data.get('DepartmentID'):
            # Giả sử model có hàm check_exists_in_table hoặc dùng execute trực tiếp
            dept_exists = self.model.execute_mssql(
                "SELECT 1 FROM Departments WHERE DepartmentID = :id", 
                {"id": data['DepartmentID']}, fetch=True
            )
            if not dept_exists:
                errors.append(f"Phòng ban ID {data['DepartmentID']} không tồn tại.")

        # 2. Kiểm tra Chức vụ (PositionID)
        if data.get('PositionID'):
            pos_exists = self.model.execute_mssql(
                "SELECT 1 FROM Positions WHERE PositionID = :id", 
                {"id": data['PositionID']}, fetch=True
            )
            if not pos_exists:
                errors.append(f"Chức vụ ID {data['PositionID']} không tồn tại.")

        # 3. Kiểm tra trùng Email/SĐT
        email = data.get('Email')
        phone = data.get('PhoneNumber')
        
        if email or phone:
            sql = "SELECT EmployeeID, FullName FROM Employees WHERE (Email = :email OR PhoneNumber = :phone)"
            params = {"email": email, "phone": phone}
            
            if is_update:
                sql += " AND EmployeeID <> :emp_id"
                params["emp_id"] = emp_id
                
            duplicate = self.model.execute_mssql(sql, params, fetch=True)
            if duplicate:
                errors.append("Email hoặc Số điện thoại đã được đăng ký cho nhân viên khác.")

        if errors:
            raise ValueError(" | ".join(errors))

    # --- HÀM VALIDATION CƠ BẢN (FORMAT) ---
    def _validate_basic_info(self, data, is_update=False):
        errors = []
        
        # 1. Check trường bắt buộc
        required = ['FullName', 'DepartmentID', 'PositionID', 'Gender']
        if not is_update:
            required += ['Email', 'PhoneNumber', 'HireDate']
            
        for field in required:
            if not data.get(field):
                errors.append(f"Thiếu {field}")

        # 2. Định dạng Email
        email = data.get('Email')
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("Email sai định dạng.")

        # 3. Định dạng SĐT (Việt Nam)
        phone = data.get('PhoneNumber')
        if phone and not re.match(r"^(0|84)[0-9]{9,10}$", str(phone)):
            errors.append("Số điện thoại phải là 10 số (bắt đầu bằng 0 hoặc 84).")

        # 4. Kiểm tra tuổi (Phải >= 18)
        dob = data.get('DateOfBirth')
        if dob:
            try:
                birth_date = datetime.strptime(dob, '%Y-%m-%d')
                age = (datetime.now() - birth_date).days // 365
                if age < 18:
                    errors.append("Nhân viên chưa đủ 18 tuổi.")
            except ValueError:
                errors.append("Ngày sinh sai định dạng YYYY-MM-DD.")

        if errors:
            raise ValueError(" | ".join(errors))

    # --- 5. CHI TIẾT ---
    def get_employee_detail_full(self, emp_id):
        try:
            res = self.model.get_full_employee_info(emp_id)
            return {"status": "success", "data": res} if res else {"status": "error", "message": "Không tìm thấy."}
        except Exception as e:
            raise e

    # --- 6. ĐỒNG BỘ ---
    def sync_all_to_payroll_system(self):
        try:
            return self.model.sync_missing_employees()
        except Exception as e:
            return {"status": "error", "message": str(e)}
    # ==========================================
    # 5. CẤP QUYỀN (ADMIN TASKS)
    # ==========================================

    def add_role_permission(self, role_id, permission_id):
        """Gán một quyền (Permission) cho một vai trò (Role)"""
        sql = """
            IF NOT EXISTS (SELECT 1 FROM [ROLE_PERMISSION] WHERE RoleID = :rid AND PermissionID = :pid)
            INSERT INTO [ROLE_PERMISSION] (RoleID, PermissionID) VALUES (:rid, :pid)
        """
        return self.execute_query(sql, {"rid": role_id, "pid": permission_id}, fetch=False)

    def remove_role_permission(self, role_id, permission_id):
        """Thu hồi quyền khỏi vai trò"""
        sql = "DELETE FROM [ROLE_PERMISSION] WHERE RoleID = :rid AND PermissionID = :pid"
        return self.execute_query(sql, {"rid": role_id, "pid": permission_id}, fetch=False)

    def add_permission_function(self, permission_id, function_id):
        """Gán một chức năng (Function) vào một quyền (Permission)"""
        sql = """
            IF NOT EXISTS (SELECT 1 FROM [PERMISSION_FUNCTION] WHERE PermissionID = :pid AND FunctionID = :fid)
            INSERT INTO [PERMISSION_FUNCTION] (PermissionID, FunctionID) VALUES (:pid, :fid)
        """
        return self.execute_query(sql, {"pid": permission_id, "fid": function_id}, fetch=False)
    
    def remove_permission_function(self, permission_id, function_id):
        """Xóa liên kết giữa quyền và chức năng"""
        sql = "DELETE FROM [PERMISSION_FUNCTION] WHERE PermissionID = :pid AND FunctionID = :fid"
        return self.execute_query(sql, {"pid": permission_id, "fid": function_id}, fetch=False)