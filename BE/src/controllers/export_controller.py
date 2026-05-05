"""
Export Controller - Controller để xuất dữ liệu
"""
from flask import send_file, request, jsonify
from src.services.export_service import ExportService
from src.models.employee_model import EmployeeModel
from src.models.salariesModel import SalaryModel
from src.models.attendenceModel import AttendanceModel
from src.utils.jwt_rbac_helper import jwt_required, roles_required
from datetime import datetime

class ExportController:
    def __init__(self):
        self.export_service = ExportService()
        self.employee_model = EmployeeModel()
        self.salary_model = SalaryModel()
        self.attendance_model = AttendanceModel()
    
    @jwt_required
    @roles_required("SUPER_ADMIN", "HR_MANAGER")
    def export_employees_excel(self, **kwargs):
        """
        GET /api/v1/export/employees/excel
        Xuất danh sách nhân viên ra Excel
        
        Query params:
            - name: Tên nhân viên (optional)
            - dept_id: ID phòng ban (optional)
            - pos_id: ID chức vụ (optional)
            - status: Trạng thái (optional)
        """
        try:
            # Get filters from query params
            name = request.args.get('name', '')
            dept_id = request.args.get('dept_id', '')
            pos_id = request.args.get('pos_id', '')
            status = request.args.get('status', '')
            gender = request.args.get('gender', '')
            start_date = request.args.get('start_date', '')
            end_date = request.args.get('end_date', '')
            
            # Get all employees (no pagination for export)
            employees_data = self.employee_model.get_employees_paged(
                page=1,
                limit=10000,  # Get all
                name=name,
                dept_id=dept_id,
                pos_id=pos_id,
                status=status,
                gender=gender,
                start_date=start_date,
                end_date=end_date
            )
            
            employees = employees_data.get('data', [])
            
            if not employees:
                return jsonify({
                    "status": "error",
                    "message": "Không có dữ liệu để xuất"
                }), 400
            
            # Export to Excel
            excel_file = self.export_service.export_employees_to_excel(employees)
            
            # Generate filename
            filename = f"Danh_sach_nhan_vien_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            return send_file(
                excel_file,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=filename
            )
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi xuất Excel: {str(e)}"
            }), 500
    
    @jwt_required
    @roles_required("SUPER_ADMIN", "HR_MANAGER")
    def export_employees_pdf(self, **kwargs):
        """
        GET /api/v1/export/employees/pdf
        Xuất danh sách nhân viên ra PDF
        
        Query params: Same as Excel
        """
        try:
            # Get filters
            name = request.args.get('name', '')
            dept_id = request.args.get('dept_id', '')
            pos_id = request.args.get('pos_id', '')
            status = request.args.get('status', '')
            gender = request.args.get('gender', '')
            start_date = request.args.get('start_date', '')
            end_date = request.args.get('end_date', '')
            
            # Get all employees
            employees_data = self.employee_model.get_employees_paged(
                page=1,
                limit=10000,
                name=name,
                dept_id=dept_id,
                pos_id=pos_id,
                status=status,
                gender=gender,
                start_date=start_date,
                end_date=end_date
            )
            
            employees = employees_data.get('data', [])
            
            if not employees:
                return jsonify({
                    "status": "error",
                    "message": "Không có dữ liệu để xuất"
                }), 400
            
            # Export to PDF
            pdf_file = self.export_service.export_employees_to_pdf(employees)
            
            # Generate filename
            filename = f"Danh_sach_nhan_vien_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            return send_file(
                pdf_file,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=filename
            )
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi xuất PDF: {str(e)}"
            }), 500
    
    @jwt_required
    @roles_required("SUPER_ADMIN", "HR_MANAGER", "PAYROLL_ACCOUNTANT")
    def export_report_excel(self, **kwargs):
        """
        POST /api/v1/export/report/excel
        Xuất báo cáo ra Excel
        
        Body:
            - report_type: Loại báo cáo (salary, attendance, etc.)
            - headers: Array of header names
            - data: Array of data rows
        """
        try:
            body = request.get_json()
            
            report_type = body.get('report_type', 'general')
            report_data = {
                'headers': body.get('headers', []),
                'data': body.get('data', [])
            }
            
            if not report_data['data']:
                return jsonify({
                    "status": "error",
                    "message": "Không có dữ liệu để xuất"
                }), 400
            
            # Export to Excel
            excel_file = self.export_service.export_report_to_excel(report_data, report_type)
            
            # Generate filename
            filename = f"Bao_cao_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            return send_file(
                excel_file,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=filename
            )
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi xuất Excel: {str(e)}"
            }), 500
    
    @jwt_required
    @roles_required("SUPER_ADMIN", "HR_MANAGER", "PAYROLL_ACCOUNTANT")
    def export_report_pdf(self, **kwargs):
        """
        POST /api/v1/export/report/pdf
        Xuất báo cáo ra PDF
        
        Body: Same as Excel
        """
        try:
            body = request.get_json()
            
            report_type = body.get('report_type', 'general')
            report_data = {
                'headers': body.get('headers', []),
                'data': body.get('data', [])
            }
            
            if not report_data['data']:
                return jsonify({
                    "status": "error",
                    "message": "Không có dữ liệu để xuất"
                }), 400
            
            # Export to PDF
            pdf_file = self.export_service.export_report_to_pdf(report_data, report_type)
            
            # Generate filename
            filename = f"Bao_cao_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            return send_file(
                pdf_file,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=filename
            )
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi xuất PDF: {str(e)}"
            }), 500

    @jwt_required
    @roles_required("SUPER_ADMIN", "HR_MANAGER", "PAYROLL_ACCOUNTANT")
    def export_salary_excel(self, **kwargs):
        """
        GET /api/v1/export/salary/excel
        Xuất dữ liệu lương ra Excel
        """
        try:
            # Get filters from query params
            month = request.args.get('month', '')
            name = request.args.get('name', '')
            dept_id = request.args.get('dept_id', '')
            pos_id = request.args.get('pos_id', '')
            status = request.args.get('status', '')
            
            # Get salary data - FIX: use correct method name
            salary_data = self.salary_model.get_salary_list(
                page=1,
                limit=10000,  # Get all
                month=month,
                name=name,
                dept_id=dept_id,
                pos_id=pos_id,
                status=status,
                sort_by='FullName',
                sort_order='ASC'
            )
            
            salaries = salary_data.get('data', [])
            
            if not salaries:
                return jsonify({
                    "status": "error",
                    "message": "Không có dữ liệu lương để xuất"
                }), 400
            
            # Export to Excel
            excel_file = self.export_service.export_salary_to_excel(salaries, month)
            
            # Generate filename
            month_str = month.replace('-', '') if month else datetime.now().strftime('%Y%m')
            filename = f"Bang_luong_{month_str}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            return send_file(
                excel_file,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=filename
            )
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi xuất Excel lương: {str(e)}"
            }), 500
    
    @jwt_required
    @roles_required("SUPER_ADMIN", "HR_MANAGER", "PAYROLL_ACCOUNTANT")
    def export_salary_pdf(self, **kwargs):
        """
        GET /api/v1/export/salary/pdf
        Xuất dữ liệu lương ra PDF
        """
        try:
            # Get filters
            month = request.args.get('month', '')
            name = request.args.get('name', '')
            dept_id = request.args.get('dept_id', '')
            pos_id = request.args.get('pos_id', '')
            status = request.args.get('status', '')
            
            # Get salary data - FIX: use correct method name
            salary_data = self.salary_model.get_salary_list(
                page=1,
                limit=10000,
                month=month,
                name=name,
                dept_id=dept_id,
                pos_id=pos_id,
                status=status,
                sort_by='FullName',
                sort_order='ASC'
            )
            
            salaries = salary_data.get('data', [])
            
            if not salaries:
                return jsonify({
                    "status": "error",
                    "message": "Không có dữ liệu lương để xuất"
                }), 400
            
            # Export to PDF
            pdf_file = self.export_service.export_salary_to_pdf(salaries, month)
            
            # Generate filename
            month_str = month.replace('-', '') if month else datetime.now().strftime('%Y%m')
            filename = f"Bang_luong_{month_str}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            return send_file(
                pdf_file,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=filename
            )
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi xuất PDF lương: {str(e)}"
            }), 500
    
    @jwt_required
    @roles_required("SUPER_ADMIN", "HR_MANAGER")
    def export_attendance_excel(self, **kwargs):
        """
        GET /api/v1/export/attendance/excel
        Xuất dữ liệu chấm công ra Excel
        """
        try:
            # Get filters from query params
            month = request.args.get('month', '')
            name = request.args.get('name', '')
            dept_id = request.args.get('dept_id', '')
            pos_id = request.args.get('pos_id', '')
            status = request.args.get('status', '')
            
            # Get attendance data - FIX: use correct method name
            attendance_data = self.attendance_model.get_full_attendance_list(
                page=1,
                limit=10000,  # Get all
                month=month,
                name=name,
                dept_id=dept_id,
                pos_id=pos_id,
                status=status,
                sort_by='FullName',
                sort_order='ASC'
            )
            
            attendances = attendance_data.get('data', [])
            
            if not attendances:
                return jsonify({
                    "status": "error",
                    "message": "Không có dữ liệu chấm công để xuất"
                }), 400
            
            # Export to Excel
            excel_file = self.export_service.export_attendance_to_excel(attendances, month)
            
            # Generate filename
            month_str = month.replace('-', '') if month else datetime.now().strftime('%Y%m')
            filename = f"Bang_cham_cong_{month_str}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            return send_file(
                excel_file,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=filename
            )
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi xuất Excel chấm công: {str(e)}"
            }), 500
    
    @jwt_required
    @roles_required("SUPER_ADMIN", "HR_MANAGER")
    def export_attendance_pdf(self, **kwargs):
        """
        GET /api/v1/export/attendance/pdf
        Xuất dữ liệu chấm công ra PDF
        """
        try:
            # Get filters
            month = request.args.get('month', '')
            name = request.args.get('name', '')
            dept_id = request.args.get('dept_id', '')
            pos_id = request.args.get('pos_id', '')
            status = request.args.get('status', '')
            
            # Get attendance data - FIX: use correct method name
            attendance_data = self.attendance_model.get_full_attendance_list(
                page=1,
                limit=10000,
                month=month,
                name=name,
                dept_id=dept_id,
                pos_id=pos_id,
                status=status,
                sort_by='FullName',
                sort_order='ASC'
            )
            
            attendances = attendance_data.get('data', [])
            
            if not attendances:
                return jsonify({
                    "status": "error",
                    "message": "Không có dữ liệu chấm công để xuất"
                }), 400
            
            # Export to PDF
            pdf_file = self.export_service.export_attendance_to_pdf(attendances, month)
            
            # Generate filename
            month_str = month.replace('-', '') if month else datetime.now().strftime('%Y%m')
            filename = f"Bang_cham_cong_{month_str}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            return send_file(
                pdf_file,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=filename
            )
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Lỗi xuất PDF chấm công: {str(e)}"
            }), 500
