from flask import jsonify, request,send_file
from src.services.salaryService import SalaryService
from datetime import datetime

class SalaryController:
    def __init__(self):
        self.service = SalaryService()

    # --- 1. GET (Danh sách lương với bộ lọc và SẮP XẾP) ---
    def get_salary_list(self):
        # Thu thập tất cả các tham số từ URL
        filters = {
            'month': request.args.get('month'),
            'name': request.args.get('name'),
            'dept_id': request.args.get('dept_id'),
            'pos_id': request.args.get('pos_id'),
            'status': request.args.get('status'),
            'page': request.args.get('page', 1),
            'limit': request.args.get('limit', 10),
            # Thêm 2 tham số sắp xếp
            'sort_by': request.args.get('sort_by', 'FullName'),
            'sort_order': request.args.get('sort_order', 'ASC')
        }

        # Service bây giờ đã nhận được sort_by và sort_order qua filters
        data = self.service.get_salary_report(filters)
        return jsonify({"status": 200, "data": data}), 200

    # --- 2, 3, 4 giữ nguyên...
    def process_salary(self):
        data = request.json
        result = self.service.process_employee_salary(data)
        status_code = 201 if result["status"] == "success" else 400
        return jsonify(result), status_code

    def update_salary(self, id):
        data = request.json
        result = self.service.update_employee_salary(id, data)
        status_code = 200 if result["status"] == "success" else 400
        return jsonify(result), status_code

    def get_salary_history(self, employee_id):
        data = self.service.get_salary_history(employee_id)
        return jsonify({"status": 200, "data": data}), 200
    def export_salary_report(self):
        # Lấy tháng từ query parameter (mặc định tháng hiện tại nếu không có)
        month = request.args.get('month', datetime.now().strftime('%Y-%m'))
        
        result = self.service.export_salary_to_excel(month)
        
        if result["status"] == "success":
            # Trả về file Excel cho trình duyệt tải xuống
            return send_file(
                result["data"],
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                download_name=f'Payroll_Report_{month}.xlsx',
                as_attachment=True
            )
        else:
            # Trả về lỗi nếu không có dữ liệu
            return jsonify(result), 400