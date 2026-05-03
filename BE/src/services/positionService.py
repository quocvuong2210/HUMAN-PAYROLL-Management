from src.models.positionModel import PositionModel

class PositionService:
    def __init__(self):
        # Khởi tạo model cho cả 2 loại database
        # MySQL đóng vai trò Slave (để đọc/thống kê)
        # MSSQL đóng vai trò Master (để ghi dữ liệu chính)
        self.db_mysql = PositionModel(db_type="mysql")
        self.db_mssql = PositionModel(db_type="mssql")

    # --- 1. NHÓM HÀM TRUY VẤN (READ) ---

    def list_all_positions(self, search_query=None):
        """
        Lấy danh sách chức vụ kèm số lượng nhân viên thực tế.
        Sử dụng db_mysql vì model đã tối ưu hàm get_positions để lấy data từ Slave.
        """
        return self.db_mysql.get_positions(search_name=search_query)

    def get_details(self, pos_id):
        """Lấy chi tiết 1 chức vụ kèm thông tin đầy đủ"""
        try:
            # Sử dụng hàm get_position_by_id đã định nghĩa trong Model
            pos = self.db_mysql.get_position_by_id(pos_id)
            
            if not pos:
                return {"status": "error", "message": "Không tìm thấy chức vụ."}
            return {"status": "success", "data": pos}
        except Exception as e:
            return {"status": "error", "message": f"Lỗi truy xuất: {str(e)}"}

    # --- 2. NHÓM HÀM THAO TÁC DỮ LIỆU ĐỒNG BỘ (CUD) ---

    def create_position_sync(self, name):
        """Thêm mới chức vụ đồng bộ 2 DB"""
        clean_name = name.strip() if name else ""
        if not clean_name:
            return {"status": "error", "message": "Tên chức vụ không được để trống."}

        try:
            # 1. Kiểm tra trùng tên trên MSSQL (Master) để đảm bảo tính duy nhất
            # Lưu ý: Model get_positions trên MSSQL đã được xử lý để lấy data thô
            existing = self.db_mssql.get_all_mssql()
            if any(p['PositionName'].lower() == clean_name.lower() for p in existing):
                return {"status": "error", "message": f"Chức vụ '{clean_name}' đã tồn tại."}

            # 2. Bước 1: Thêm vào MSSQL (Master) và lấy ID tự tăng
            res_mssql = self.db_mssql.add_position_mssql(clean_name)
            if not res_mssql:
                return {"status": "error", "message": "Lỗi tạo dữ liệu trên SQL Server Master."}
            
            new_id = res_mssql[0]['PositionID']

            # 3. Bước 2: Đẩy ID và Name đó sang MySQL (Slave) ngay lập tức
            self.db_mysql.add_position_mysql(new_id, clean_name)
            
            return {
                "status": "success", 
                "message": f"Đã thêm chức vụ '{clean_name}' thành công.",
                "data": {"id": new_id, "name": clean_name}
            }
        except Exception as e:
            return {"status": "error", "message": f"Lỗi đồng bộ: {str(e)}"}

    def update_info(self, pos_id, new_name):
        """Cập nhật tên chức vụ trên cả 2 hệ thống"""
        clean_name = new_name.strip() if new_name else ""
        if not clean_name:
            return {"status": "error", "message": "Tên mới không hợp lệ."}

        try:
            # 1. Kiểm tra tên mới có bị trùng ở ID khác không (Tránh rename trùng tên)
            all_pos = self.db_mssql.get_all_mssql()
            if any(p['PositionName'].lower() == clean_name.lower() and p['PositionID'] != int(pos_id) for p in all_pos):
                return {"status": "error", "message": f"Tên '{clean_name}' đã được dùng cho chức vụ khác."}

            # 2. Cập nhật đồng bộ cả 2 bên
            self.db_mssql.update_position(pos_id, clean_name)
            self.db_mysql.update_position(pos_id, clean_name)
            
            return {"status": "success", "message": "Cập nhật chức vụ thành công trên toàn hệ thống."}
        except Exception as e:
            return {"status": "error", "message": f"Lỗi cập nhật: {str(e)}"}

    def remove_position(self, pos_id):
        """Xóa chức vụ kèm kiểm tra ràng buộc nhân viên cực kỳ chặt chẽ"""
        try:
            # 1. RÀNG BUỘC: Kiểm tra xem có nhân viên nào đang giữ chức vụ này không
            # Kiểm tra ở MySQL (Slave) vì đây là nơi lưu trữ bảng nhân viên đồng bộ
            check_sql = "SELECT COUNT(*) as total FROM employees_payroll WHERE PositionID = :id"
            usage = self.db_mysql.execute_query(check_sql, params={"id": pos_id}, fetch=True)
            
            if usage and usage[0]['total'] > 0:
                return {
                    "status": "error", 
                    "message": f"Không thể xóa: Hiện đang có {usage[0]['total']} nhân viên đang giữ chức vụ này. Vui lòng chuyển nhân viên sang chức vụ khác trước."
                }

            # 2. Thực hiện xóa 2 bên (Xóa ở Master trước, Slave sau)
            self.db_mssql.delete_position(pos_id)
            self.db_mysql.delete_position(pos_id)

            return {"status": "success", "message": "Đã xóa chức vụ thành công."}
        except Exception as e:
            return {"status": "error", "message": f"Lỗi hệ thống khi xóa: {str(e)}"}

    # --- 3. TIỆN ÍCH HỆ THỐNG ---

    def force_sync_from_master(self):
        """
        Nạp toàn bộ dữ liệu từ MSSQL vào MySQL.
        Dùng cho nút 'Refresh' hoặc 'Sync' trên UI khi dữ liệu bị lệch.
        """
        try:
            # Lấy data thô từ Master
            all_mssql = self.db_mssql.get_all_mssql()
            count = 0
            for pos in all_mssql:
                # Sử dụng logic ON DUPLICATE KEY UPDATE trong model để đồng bộ
                self.db_mysql.add_position_mysql(pos['PositionID'], pos['PositionName'])
                count += 1
            return {"status": "success", "message": f"Đã đồng bộ hoàn tất {count} chức vụ từ Master sang Slave."}
        except Exception as e:
            return {"status": "error", "message": f"Lỗi đồng bộ thủ công: {str(e)}"}