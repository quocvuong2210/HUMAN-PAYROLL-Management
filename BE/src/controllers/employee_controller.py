from flask import jsonify, request
from src.services.employee_service import EmployeeService

class EmployeeController:
    def __init__(self):
        self.service = EmployeeService()

    # --- 1. LẤY DANH SÁCH + PHÂN TRANG + FULL FILTERS ---
    def get_employees(self):
        """
        Hứng toàn bộ params từ URL:
        ?name=...&dept_id=...&pos_id=...&status=...&gender=...&start_date=...&end_date=...&page=...&limit=...
        """
        try:
            filters = {
                # Các bộ lọc tìm kiếm
                'name': request.args.get('name'),
                'dept_id': request.args.get('dept_id'),
                'pos_id': request.args.get('pos_id'),      # Mới: Lọc theo chức vụ
                'status': request.args.get('status'),
                'gender': request.args.get('gender'),      # Mới: Lọc theo giới tính
                'start_date': request.args.get('start_date'), # Mới: Ngày bắt đầu
                'end_date': request.args.get('end_date'),     # Mới: Ngày kết thúc
                
                # Tham số phân trang
                'page': request.args.get('page', default=1, type=int),
                'limit': request.args.get('limit', default=10, type=int)
            }
            
            result = self.service.list_employees(filters)
            
            return jsonify({
                "status": 200,
                "message": "Lấy danh sách thành công",
                "total_records": result['total_records'],
                "total_pages": result['total_pages'],
                "current_page": result['current_page'],
                "limit": result['limit'],
                "data": result['data']
            }), 200
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500
# --- 7. ĐỒNG BỘ TOÀN BỘ DỮ LIỆU (NEW ENDPOINT) ---
    def sync_all(self):
        """
        Endpoint để Frontend bấm nút 'Đồng bộ hệ thống'
        POST /api/v1/employees/sync
        """
        try:
            # Gọi service thực hiện quét và đẩy dữ liệu sang MySQL
            result = self.service.sync_all_to_payroll_system()
            
            status_code = 200 if result.get("status") == "success" else 500
            return jsonify(result), status_code
        except Exception as e:
            return jsonify({
                "status": "error", 
                "message": f"Lỗi thực thi đồng bộ: {str(e)}"
            }), 500

    # --- TỐI ƯU HÀM ADD/UPDATE ĐỂ TRẢ VỀ MESSAGE RÕ RÀNG HƠN ---
    def add_employee(self):
        try:
            data = request.json
            if not data:
                return jsonify({"status": "error", "message": "Dữ liệu không được để trống"}), 400

            result = self.service.create_employee(data)
            
            # Nếu Service trả về lỗi validation (status: error)
            if result.get("status") == "error":
                return jsonify(result), 400
                
            return jsonify(result), 201
        except Exception as e:
            # Ghi log lỗi chi tiết tại server, chỉ trả về thông báo ngắn gọn cho client
            
            print(f"Critial Error: {str(e)}")
            return jsonify({"status": "error", "message": "Lỗi hệ thống khi tạo nhân viên."}), 500

    # --- 3. CẬP NHẬT ---
    def update_employee(self, id):
        try:
            data = request.json
            if not data:
                return jsonify({"status": 400, "message": "Dữ liệu cập nhật trống"}), 400

            result = self.service.update_employee(id, data)
            
            status_code = 200 if result.get("status") == "success" else 400
            return jsonify(result), status_code
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500

    # --- 4. XÓA (XÓA SẠCH 2 DATABASE) ---
    def delete_employee(self, id):
        try:
            result = self.service.delete_employee(id)
            
            if result.get("status") == "warning":
                return jsonify(result), 404
            
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500

    # --- 5. CHI TIẾT (HỒ SƠ + LƯƠNG + CHUYÊN CẦN) ---
    def get_employee_detail(self, id):
        try:
            result = self.service.get_employee_detail_full(id)
            
            if result.get("status") == "error":
                return jsonify(result), 404
                
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500

    # --- 6. METADATA (DÙNG CHO FORM & SEARCH) ---
    def get_metadata(self):
        """Lấy danh sách Departments và Positions từ MSSQL để Frontend hiển thị Select Box"""
        try:
            departments = self.service.model.get_departments()
            positions = self.service.model.get_positions()
            
            return jsonify({
                "status": 200,
                "data": {
                    "departments": departments,
                    "positions": positions,
                    "statuses": ["Đang làm việc", "Thử việc", "Nghỉ phép", "Thực tập", "Đã nghỉ việc"],
                    "genders": ["Nam", "Nữ", "Khác"]
                }
            }), 200
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500