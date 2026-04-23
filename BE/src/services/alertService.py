from src.models.alertModel import AlertModel

class AlertService:
    def __init__(self):
        self.mysql_model = AlertModel(db_type="mysql")
        self.mssql_model = AlertModel(db_type="mssql")

    def get_only_birthdays(self, month): return self.mssql_model.get_birthdays(month)
    def get_only_anniversaries(self, month): return self.mssql_model.get_work_anniversaries(month)
    def get_only_high_absence(self, month, year): return self.mysql_model.get_high_absenteeism(month, year)
    def get_only_unusual_salaries(self, month, year): return self.mysql_model.get_unusual_salaries(month, year)
    def get_only_missing_attendance(self, month, year): return self.mysql_model.get_missing_attendance(month, year)
    def get_employee_details(self, employee_id): return self.mysql_model.get_employee_details(employee_id)