"""
Export Routes - Routes cho chức năng xuất dữ liệu
"""
from flask import Blueprint
from src.controllers.export_controller import ExportController

export_bp = Blueprint('export', __name__)
export_controller = ExportController()

# ==================== EMPLOYEE EXPORT ROUTES ====================
@export_bp.route('/employees/excel', methods=['GET', 'OPTIONS'])
def export_employees_excel():
    """
    GET /api/v1/export/employees/excel
    Xuất danh sách nhân viên ra Excel
    
    Query params:
        - name: Tên nhân viên (optional)
        - dept_id: ID phòng ban (optional)
        - pos_id: ID chức vụ (optional)
        - status: Trạng thái (optional)
        - gender: Giới tính (optional)
        - start_date: Ngày bắt đầu (optional)
        - end_date: Ngày kết thúc (optional)
    
    Returns:
        Excel file (.xlsx)
    
    Permissions:
        - SUPER_ADMIN
        - HR_MANAGER
    """
    return export_controller.export_employees_excel()

@export_bp.route('/employees/pdf', methods=['GET', 'OPTIONS'])
def export_employees_pdf():
    """
    GET /api/v1/export/employees/pdf
    Xuất danh sách nhân viên ra PDF
    
    Query params: Same as Excel
    
    Returns:
        PDF file (.pdf)
    
    Permissions:
        - SUPER_ADMIN
        - HR_MANAGER
    """
    return export_controller.export_employees_pdf()

# ==================== REPORT EXPORT ROUTES ====================
@export_bp.route('/report/excel', methods=['POST', 'OPTIONS'])
def export_report_excel():
    """
    POST /api/v1/export/report/excel
    Xuất báo cáo ra Excel
    
    Body:
        {
            "report_type": "salary|attendance|general",
            "headers": ["Header1", "Header2", ...],
            "data": [
                ["value1", "value2", ...],
                ["value1", "value2", ...]
            ]
        }
    
    Returns:
        Excel file (.xlsx)
    
    Permissions:
        - SUPER_ADMIN
        - HR_MANAGER
        - PAYROLL_ACCOUNTANT
    """
    return export_controller.export_report_excel()

@export_bp.route('/report/pdf', methods=['POST', 'OPTIONS'])
def export_report_pdf():
    """
    POST /api/v1/export/report/pdf
    Xuất báo cáo ra PDF
    
    Body: Same as Excel
    
    Returns:
        PDF file (.pdf)
    
    Permissions:
        - SUPER_ADMIN
        - HR_MANAGER
        - PAYROLL_ACCOUNTANT
    """
    return export_controller.export_report_pdf()

# ==================== SALARY EXPORT ROUTES ====================
@export_bp.route('/salary/excel', methods=['GET', 'OPTIONS'])
def export_salary_excel():
    """
    GET /api/v1/export/salary/excel
    Xuất dữ liệu lương ra Excel
    
    Query params:
        - month: Tháng (YYYY-MM-DD format)
        - name: Tên nhân viên (optional)
        - dept_id: ID phòng ban (optional)
        - pos_id: ID chức vụ (optional)
        - status: Trạng thái (optional)
    
    Returns:
        Excel file (.xlsx)
    
    Permissions:
        - SUPER_ADMIN
        - HR_MANAGER
        - PAYROLL_ACCOUNTANT
    """
    return export_controller.export_salary_excel()

@export_bp.route('/salary/pdf', methods=['GET', 'OPTIONS'])
def export_salary_pdf():
    """
    GET /api/v1/export/salary/pdf
    Xuất dữ liệu lương ra PDF
    
    Query params: Same as Excel
    
    Returns:
        PDF file (.pdf)
    
    Permissions:
        - SUPER_ADMIN
        - HR_MANAGER
        - PAYROLL_ACCOUNTANT
    """
    return export_controller.export_salary_pdf()

# ==================== ATTENDANCE EXPORT ROUTES ====================
@export_bp.route('/attendance/excel', methods=['GET', 'OPTIONS'])
def export_attendance_excel():
    """
    GET /api/v1/export/attendance/excel
    Xuất dữ liệu chấm công ra Excel
    
    Query params:
        - month: Tháng (YYYY-MM-DD format)
        - name: Tên nhân viên (optional)
        - dept_id: ID phòng ban (optional)
        - pos_id: ID chức vụ (optional)
        - status: Trạng thái (optional)
    
    Returns:
        Excel file (.xlsx)
    
    Permissions:
        - SUPER_ADMIN
        - HR_MANAGER
    """
    return export_controller.export_attendance_excel()

@export_bp.route('/attendance/pdf', methods=['GET', 'OPTIONS'])
def export_attendance_pdf():
    """
    GET /api/v1/export/attendance/pdf
    Xuất dữ liệu chấm công ra PDF
    
    Query params: Same as Excel
    
    Returns:
        PDF file (.pdf)
    
    Permissions:
        - SUPER_ADMIN
        - HR_MANAGER
    """
    return export_controller.export_attendance_pdf()
