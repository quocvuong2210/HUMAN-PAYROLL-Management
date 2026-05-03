from flask import jsonify, request
from src.services.reportService import ReportService

class ReportController:
    def __init__(self):
        self.service = ReportService()

    # --- HÀM TIỆN ÍCH LẤY THAM SỐ ---
    def _get_filters(self):
        """Lấy tháng và năm từ query parameters"""
        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)
        return month, year

    # =========================================
    # 1. DASHBOARD (FULL)
    # =========================================
    def get_dashboard(self):
        month, year = self._get_filters()
        return jsonify(self.service.get_dashboard(month=month, year=year)), 200

    # =========================================
    # 2. SALARY BY DEPARTMENT
    # =========================================
    def get_salary_by_department(self):
        month, year = self._get_filters()
        return jsonify(self.service.get_salary_by_department(month=month, year=year)), 200

    # =========================================
    # 3. EMPLOYEE DISTRIBUTION (Không cần lọc)
    # =========================================
    def get_employee_distribution(self):
        return jsonify(self.service.get_employee_distribution()), 200

    # =========================================
    # 4. POSITION REPORT (Không cần lọc)
    # =========================================
    def get_position_report(self):
        return jsonify(self.service.get_position_report()), 200

    # =========================================
    # 5. ATTENDANCE REPORT
    # =========================================
    def get_attendance_report(self):
        month, year = self._get_filters()
        return jsonify(self.service.get_attendance_report(month=month, year=year)), 200

    # =========================================
    # 6. PAYROLL DETAIL
    # =========================================
    def get_payroll_detail(self):
        month, year = self._get_filters()
        return jsonify(self.service.get_payroll_detail(month=month, year=year)), 200

    # =========================================
    # 7. ALERT REPORT
    # =========================================
    def get_alert_report(self):
        month, year = self._get_filters()
        return jsonify(self.service.get_alert_report(month=month, year=year)), 200

    # =========================================
    # 8. TOP DEPARTMENT (TỐN NHẤT)
    # =========================================
    def get_top_department(self):
        month, year = self._get_filters()
        return jsonify(self.service.get_top_department(month=month, year=year)), 200

    # =========================================
    # 9. BEST EMPLOYEE
    # =========================================
    def get_best_employee(self):
        month, year = self._get_filters()
        return jsonify(self.service.get_best_employee(month=month, year=year)), 200
    