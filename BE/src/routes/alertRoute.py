from flask import Blueprint
from src.controllers.alertController import AlertController

alert_bp = Blueprint("alerts", __name__)
controller = AlertController()

@alert_bp.route("/employee/<string:employee_id>", methods=["GET"])
def get_employee_details(employee_id):
    return controller.get_employee_by_id(employee_id)

# --- CÁC THÔNG BÁO ---
@alert_bp.route("/birthdays", methods=["GET"])
def get_birthdays():
    return controller.get_birthdays()

@alert_bp.route("/anniversaries", methods=["GET"])
def get_anniversaries():
    """Endpoint: /api/v1/alerts/anniversaries?month=4"""
    return controller.get_anniversaries()

@alert_bp.route("/absenteeism", methods=["GET"])
def get_absenteeism():
    return controller.get_absenteeism()

@alert_bp.route("/unusual-salaries", methods=["GET"])
def get_unusual_salaries():
    return controller.get_unusual_salaries()
