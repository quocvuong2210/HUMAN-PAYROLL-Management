from flask import jsonify, request
from src.services.alertService import AlertService
from datetime import datetime

class AlertController:
    def __init__(self):
        self.service = AlertService()
    def get_absenteeism(self):
        try:
            m = request.args.get('month', default=datetime.now().month, type=int)
            y = request.args.get('year', default=datetime.now().year, type=int)
            data = self.service.get_only_high_absence(m, y) or []
            
            for item in data:
                absent = item.get('AbsentDays', 0)
                item['alert_level'] = "CRITICAL" if absent > 2 else "WARNING"
                item['status_color'] = "red" if item['alert_level'] == "CRITICAL" else "orange"
                item['display_msg'] = f"Nghỉ {item.get('TotalOff', 0)} ngày ({absent} ko phép)"
            return jsonify({"status": 200, "data": data}), 200
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500

    def get_anniversaries(self):
        try:
            m = request.args.get('month', default=datetime.now().month, type=int)
            data = self.service.get_only_anniversaries(m) or []
            return jsonify({"status": 200, "data": data}), 200
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500

    def get_unusual_salaries(self):
        try:
            m = request.args.get('month', default=datetime.now().month, type=int)
            y = request.args.get('year', default=datetime.now().year, type=int)
            data = self.service.get_only_unusual_salaries(m, y) or []
            for s in data:
                net = s.get('NetSalary', 0)
                s['net_salary_fmt'] = "{:,.0f} VNĐ".format(net)
                s['reason'] = "Khấu trừ > 20% lương" if s.get('Deductions', 0) > (s.get('BaseSalary', 0) * 0.2) else ("Thu nhập cao" if net > 50000000 else "Bất thường")
            return jsonify({"status": 200, "data": data}), 200
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500

    def get_employee_by_id(self, emp_id):
        try:
            data = self.service.get_employee_details(emp_id)
            if not data:
                return jsonify({"status": 404, "message": f"Không tìm thấy nhân viên ID: {emp_id}"}), 404
            
            # Định dạng lại tiền tệ cho lịch sử lương
            if 'salary_history' in data:
                for s in data['salary_history']:
                    s['net_fmt'] = "{:,.0f}đ".format(s.get('NetSalary', 0))
                    
            return jsonify({"status": 200, "data": data}), 200
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500

    def get_birthdays(self):
        try:
            m = request.args.get('month', default=datetime.now().month, type=int)
            data = self.service.get_only_birthdays(m) or []
            return jsonify({"status": 200, "data": data}), 200
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500