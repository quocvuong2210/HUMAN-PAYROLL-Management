from flask import jsonify, request
from src.services.dashboardService import DashboardService
from datetime import datetime

class DashboardController:
    def __init__(self):
        self.service = DashboardService()

    def get_all_salaries(self):
        try:
            data = self.service.get_all_salaries()
            return jsonify({
                "status": 200,
                "message": "Lấy dữ liệu lương thành công",
                "data": data
            }), 200
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500

    def get_all_employees(self):
        try:
            data = self.service.get_all_employees()
            return jsonify({
                "status": 200,
                "message": "Lấy danh sách nhân viên thành công",
                "data": data
            }), 200
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500

    def get_dashboard_summary(self):
        try:
           

            data = self.service.get_dashboard_summary()
            if data is None: data = {}

            return jsonify({
                "status": 200,
                
                "data": {
                    "total_employees": data.get('total_employees'),
                    "total_departments": data.get('total_departments'),
                    "total_net_salary": float(data.get('total_net_salary')),
                    "total_bonus": float(data.get('total_bonus') ),
                    "total_deductions": float(data.get('total_deductions')),
                    
                }
            }), 200
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500

    def get_charts(self):
        try:
            month = request.args.get('month', type=int)
            year = request.args.get('year', default=datetime.now().year, type=int)

            data = self.service.get_chart_data(month, year)
            
            return jsonify({
                "status": 200,
                "charts": {
                    "bar_chart": [
                        {"department": i.get('DepartmentName', 'N/A'), "total": float(i.get('TotalSalary', 0))} 
                        for i in data.get('salary_by_dept', [])
                    ],
                    "line_chart": [
                        {"month": f"T{i.get('Month')}", "salary": float(i.get('TotalSalary', 0))} 
                        for i in data.get('salary_trend', [])
                    ],
                    "pie_chart": [
                        {"status": i.get('Status', 'Khác'), "value": i.get('Count', 0)} 
                        for i in data.get('status_distribution', [])
                    ]
                }
            }), 200
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500

    def get_attendance_stats(self):
        try:
            month = request.args.get('month', type=int)
            year = request.args.get('year', default=datetime.now().year, type=int)

            if not month:
                return jsonify({"status": 400, "message": "Vui lòng chọn tháng"}), 400

            data = self.service.get_attendance_report(month, year)
            
            return jsonify({
                "status": 200,
                "data": {
                    "average_workdays": round(float(data.get('avg_workdays', 0)), 1),
                    "most_diligent_employees": [
                        {"name": i.get('FullName', 'N/A'), "days": i.get('WorkDays', 0)} 
                        for i in data.get('top_diligent', [])
                    ],
                    "most_absent_employees": [
                        {"name": i.get('FullName', 'N/A'), "off_days": int(i.get('TotalOff', 0))} 
                        for i in data.get('top_absent', [])
                    ]
                }
            }), 200
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500

    def get_alerts(self):
        try:
            month = request.args.get('month', type=int)
            year = request.args.get('year', default=datetime.now().year, type=int)
            
            if not month:
                return jsonify({"status": 400, "message": "Cần chọn tháng để quét cảnh báo"}), 400
                
            raw_alerts = self.service.get_system_alerts(month, year)
            alerts_list = []
            seen_contents = set()

            # 1. Nghỉ quá phép (DANGER)
            for emp in raw_alerts.get('high_absence', []):
                content = f"Nhân viên {emp['FullName']} ({emp.get('DepartmentName', 'BP')}) đã nghỉ {emp['TotalOff']} ngày."
                if content not in seen_contents:
                    alerts_list.append({"type": "danger", "title": "Nghỉ quá phép", "content": content})
                    seen_contents.add(content)

            # 2. Thiếu chấm công (WARNING)
            for emp in raw_alerts.get('missing_data', []):
                content = f"Nhân viên {emp['FullName']} chưa có dữ liệu chấm công tháng {month}."
                if content not in seen_contents:
                    alerts_list.append({"type": "warning", "title": "Thiếu chấm công", "content": content})
                    seen_contents.add(content)

            # 3. Lương bất thường (INFO/WARNING)
            for emp in raw_alerts.get('unusual_salary', []):
                content = f"Lương {emp['FullName']} có biến động (Khấu trừ: {emp.get('Deductions', 0):,.0f}đ)."
                if content not in seen_contents:
                    alerts_list.append({"type": "warning", "title": "Lương bất thường", "content": content})
                    seen_contents.add(content)

            return jsonify({
                "status": 200,
                "total_alerts": len(alerts_list),
                "data": alerts_list
            }), 200
        except Exception as e:
            return jsonify({"status": 500, "error": str(e)}), 500