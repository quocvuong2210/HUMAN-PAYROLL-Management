from src.models.departmentModel import DepartmentModel

class DepartmentService:
    def __init__(self):
        # MySQL dùng để READ (có stats), MSSQL dùng để WRITE (Master)
        self.db_mysql = DepartmentModel(db_type="mysql")
        self.db_mssql = DepartmentModel(db_type="mssql")

    # --- TRUY VẤN (SỬA ĐỔI ĐỂ HIỆN SỐ TIỀN & NHÂN VIÊN) ---

    def list_all_departments(self, search_query=None, sort_column="DepartmentID", order_dir="ASC"):
        """Lấy danh sách từ MySQL kèm thống kê nhân sự và lương"""
        return self.db_mysql.get_departments_with_stats(
            search_name=search_query, 
            sort_by=sort_column, 
            order=order_dir
        )

    def get_details(self, dept_id):
        return self.db_mysql.get_department_by_id(dept_id)

    # --- THAO TÁC DỮ LIỆU ĐỒNG BỘ ---

    def create_department_sync(self, name):
        clean_name = name.strip() if name else ""
        if not clean_name:
            return {"status": "error", "message": "Tên không được để trống."}
        
        try:
            # 1. Kiểm tra trùng tên trên Master
            existing = self.db_mssql.get_all_mssql()
            if any(d['DepartmentName'].lower() == clean_name.lower() for d in existing):
                return {"status": "error", "message": f"Phòng ban '{clean_name}' đã tồn tại."}

            # 2. Ghi Master và lấy ID
            res_mssql = self.db_mssql.add_department_mssql(clean_name)
            new_id = res_mssql[0]['DepartmentID']

            # 3. Đồng bộ ngay sang MySQL
            self.db_mysql.add_department_mysql(new_id, clean_name)
            
            return {"status": "success", "message": "Thêm và đồng bộ thành công.", "data": {"id": new_id}}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_info(self, dept_id, new_name):
        clean_name = new_name.strip() if new_name else ""
        try:
            # Cập nhật cả 2 DB
            self.db_mssql.update_department(dept_id, clean_name)
            self.db_mysql.update_department(dept_id, clean_name)
            return {"status": "success", "message": "Cập nhật thành công."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def remove_department(self, dept_id):
        """Xóa kèm kiểm tra ràng buộc nhân viên"""
        try:
            # Kiểm tra xem có nhân viên không từ hàm stats
            stats = self.db_mysql.get_departments_with_stats()
            target = next((item for item in stats if item['DepartmentID'] == int(dept_id)), None)
            
            if target and target['TotalEmployees'] > 0:
                return {"status": "error", "message": f"Không thể xóa phòng đang có {target['TotalEmployees']} nhân viên."}

            self.db_mssql.delete_department(dept_id)
            self.db_mysql.delete_department(dept_id)
            return {"status": "success", "message": "Xóa thành công."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def sync_all_from_mssql(self):
        """Đồng bộ lại toàn bộ từ MSSQL sang MySQL"""
        try:
            all_mssql = self.db_mssql.get_all_mssql()
            for dept in all_mssql:
                self.db_mysql.add_department_mysql(dept['DepartmentID'], dept['DepartmentName'])
            return {"status": "success", "message": "Đồng bộ hoàn tất."}
        except Exception as e:
            return {"status": "error", "message": str(e)}