from src.models.reportModel import ReportModel

class ReportService:
    def __init__(self):
        self.model = ReportModel()

    # --- FORMAT RESPONSE CHUNG ---
    def _success(self, data):
        return {"status": "success", "data": data}

    def _error(self, e):
        return {"status": "error", "message": str(e)}

    # =========================================
    # 1. SALARY BY DEPARTMENT (Cần lọc)
    # =========================================
    def get_salary_by_department(self, month=None, year=None):
        try:
            data = self.model.salary_by_department(month=month, year=year)
            return self._success(data)
        except Exception as e:
            return self._error(e)

    # =========================================
    # 2. EMPLOYEE DISTRIBUTION (Không cần lọc)
    # =========================================
    def get_employee_distribution(self):
        try:
            data = self.model.employee_distribution()
            return self._success(data)
        except Exception as e:
            return self._error(e)

    # =========================================
    # 3. POSITION REPORT (Không cần lọc)
    # =========================================
    def get_position_report(self):
        try:
            data = self.model.position_report()
            return self._success(data)
        except Exception as e:
            return self._error(e)

    # =========================================
    # 4. ATTENDANCE REPORT (Cần lọc)
    # =========================================
    def get_attendance_report(self, month=None, year=None):
        try:
            data = self.model.attendance_report(month=month, year=year)
            return self._success(data)
        except Exception as e:
            return self._error(e)

    # =========================================
    # 5. PAYROLL DETAIL (Cần lọc)
    # =========================================
    def get_payroll_detail(self, month=None, year=None):
        try:
            data = self.model.payroll_detail(month=month, year=year)
            return self._success(data)
        except Exception as e:
            return self._error(e)

    # =========================================
    # 6. ALERT REPORT (Cần lọc)
    # =========================================
    def get_alert_report(self, month=None, year=None):
        try:
            data = self.model.alert_report(month=month, year=year)
            return self._success(data)
        except Exception as e:
            return self._error(e)

    # =========================================
    # 7. TOP DEPARTMENT (Cần lọc)
    # =========================================
    def get_top_department(self, month=None, year=None):
        try:
            # Model của bạn đặt tên hàm này là department_cost
            data = self.model.department_cost(month=month, year=year)
            return self._success(data)
        except Exception as e:
            return self._error(e)

    # =========================================
    # 8. BEST EMPLOYEE (Cần lọc)
    # =========================================
    def get_best_employee(self, month=None, year=None):
        try:
            data = self.model.best_employee(month=month, year=year)
            return self._success(data)
        except Exception as e:
            return self._error(e)

    # =========================================
    # 9. FULL DASHBOARD (Cần lọc)
    # =========================================
    def get_dashboard(self, month=None, year=None):
        try:
            data = self.model.dashboard(month=month, year=year)
            return self._success(data)
        except Exception as e:
            return self._error(e)