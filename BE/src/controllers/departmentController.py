from flask import jsonify, request
from src.services.departmentService import DepartmentService

class DepartmentController:
    def __init__(self):
        # Service quản lý logic giữa MSSQL (Master) và MySQL (Slave)
        self.service = DepartmentService()

    def get_all_departments(self):
        """
        Lấy danh sách phòng ban đầy đủ thông tin:
        - Tên phòng, ID
        - Số lượng nhân viên (TotalEmployees)
        - Tổng quỹ lương (TotalSalary)
        """
        try:
            # Lấy tham số từ URL query string
            search_query = request.args.get('search', default=None, type=str)
            sort_column = request.args.get('sort', default='DepartmentID', type=str)
            order_dir = request.args.get('order', default='ASC', type=str).upper()

            # Gọi service (Service này đã được sửa để lấy stats từ MySQL)
            data = self.service.list_all_departments(search_query, sort_column, order_dir)
            
            return jsonify({
                "status": 200,
                "message": "Lấy danh sách phòng ban và thống kê thành công",
                "count": len(data),
                "data": data
            }), 200
        except Exception as e:
            return jsonify({"status": 500, "error": f"Lỗi Controller: {str(e)}"}), 500

    def get_department_by_id(self, dept_id):
        """Chi tiết một phòng ban"""
        try:
            data = self.service.get_details(dept_id)
            if isinstance(data, dict) and data.get("status") == "error":
                return jsonify(data), 404
            
            return jsonify({
                "status": 200,
                "data": data
            }), 200
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500

    def create_department(self):
        """Thêm mới đồng bộ cả 2 Database"""
        try:
            body = request.get_json()
            name = body.get('DepartmentName')

            if not name:
                return jsonify({"status": 400, "message": "Tên phòng ban là bắt buộc"}), 400

            result = self.service.create_department_sync(name)
            
            status_code = 201 if result["status"] == "success" else 400
            return jsonify(result), status_code
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500

    def update_department(self, dept_id):
        """Cập nhật tên phòng ban đồng bộ"""
        try:
            body = request.get_json()
            new_name = body.get('DepartmentName')

            if not new_name:
                return jsonify({"status": 400, "message": "Tên mới là bắt buộc"}), 400

            result = self.service.update_info(dept_id, new_name)
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500

    def delete_department(self, dept_id):
        """Xóa phòng ban (có kiểm tra ràng buộc nhân viên trong service)"""
        try:
            result = self.service.remove_department(dept_id)
            status_code = 200 if result["status"] == "success" else 400
            return jsonify(result), status_code
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500

    def sync_data(self):
        """Force sync từ MSSQL sang MySQL"""
        try:
            result = self.service.sync_all_from_mssql()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500