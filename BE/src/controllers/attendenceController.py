from flask import jsonify, request
from src.services.attendenceService import AttendanceService

class AttendanceController:
    def __init__(self):
        self.service = AttendanceService()

    # --- GET (Danh sách chấm công) ---
    def get_attendance(self):
        filters = {
            'month': request.args.get('month'),
            'name': request.args.get('name'),
            'dept_id': request.args.get('dept_id'),
            'pos_id': request.args.get('pos_id'),
            'status': request.args.get('status'),
            
            'page': request.args.get('page', 1),   # Nhận page từ query string
            'limit': request.args.get('limit', 10), # Nhận limit từ query string
            'sort_by': request.args.get('sort_by', 'FullName'),
            'sort_order': request.args.get('sort_order', 'ASC')
        }

        data = self.service.get_attendance_report(filters)
        return jsonify({"status": 200, "data": data}), 200

    # --- POST (Thêm mới) ---
    def add_attendance(self):
        data = request.json
        result = self.service.record_employee_attendance(data)

        status_code = 201 if result["status"] == "success" else 400
        return jsonify(result), status_code

    # --- MISSING (Chưa chấm công) ---
    def get_missing_attendance(self):
        filters = {
            'month': request.args.get('month'),
            'name': request.args.get('name'),
            'dept_id': request.args.get('dept_id'),
            'page': request.args.get('page', 1),
            'limit': request.args.get('limit', 10)
        }

        data = self.service.list_missing_attendance(filters)
        return jsonify({"status": 200, "data": data}), 200

    # --- PUT (Cập nhật) ---
    def update_attendance(self, id):
        data = request.json
        result = self.service.update_attendance(id, data)

        status_code = 200 if result["status"] == "success" else 400
        return jsonify(result), status_code