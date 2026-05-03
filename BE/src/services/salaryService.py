import pandas as pd
import io
from src.models.salariesModel import SalaryModel
from datetime import datetime
class SalaryService:
    def __init__(self):
        self.model = SalaryModel()

    # --- 1. LẤY BÁO CÁO LƯƠNG (FULL FILTER, PAGINATION & SORTING) ---
    def get_salary_report(self, filters):
        # Lấy page/limit/sort từ filters
        page = int(filters.get('page', 1))
        limit = int(filters.get('limit', 10))
        
        # Lấy tham số sắp xếp (nếu không có thì mặc định theo Tên)
        sort_by = filters.get('sort_by', 'FullName')
        sort_order = filters.get('sort_order', 'ASC')
        
        return self.model.get_salary_list(
            month=filters.get('month'),
            name=filters.get('name'),
            dept_id=filters.get('dept_id'),
            pos_id=filters.get('pos_id'),
            status=filters.get('status'),
            page=page,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order
        )

    # --- 2. TÍNH LƯƠNG CHO MỘT NHÂN VIÊN ---
    def process_employee_salary(self, data):
        try:
            emp_id = data.get('EmployeeID')
            month = data.get('SalaryMonth', datetime.now().strftime('%Y-%m-01'))
            
            # Kiểm tra trạng thái trước khi tính
            if self.model.check_employee_salary_status(emp_id, month):
                return {"status": "error", "message": "Lương tháng này đã được tính cho nhân viên này."}

            base_salary = float(data.get('BaseSalary', 0))
            bonus = float(data.get('Bonus', 0))
            deductions = float(data.get('Deductions', 0))

            self.model.process_salary(emp_id, month, base_salary, bonus, deductions)
            return {"status": "success", "message": "Tính lương thành công"}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # --- 3. CẬP NHẬT LƯƠNG ---
    def update_employee_salary(self, salary_id, data):
        try:
            base_salary = float(data.get('BaseSalary', 0))
            bonus = float(data.get('Bonus', 0))
            deductions = float(data.get('Deductions', 0))

            affected = self.model.update_salary(salary_id, base_salary, bonus, deductions)
            
            if affected > 0:
                return {"status": "success", "message": "Cập nhật thành công"}
            return {"status": "error", "message": "Không tìm thấy bản ghi lương"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # --- 4. LẤY LỊCH SỬ LƯƠNG ---
    def get_salary_history(self, employee_id):
        return self.model.get_employee_salary_history(employee_id)
    def export_salary_to_excel(self, month):
        try:
            # 1. Lấy dữ liệu tổng hợp
            data = self.model.get_full_payroll_data(month)
            if not data:
                return {"status": "error", "message": "Không có dữ liệu cho tháng này"}

            # 2. Tạo DataFrame từ dữ liệu
            df = pd.DataFrame(data)

            # 3. Rename các cột để hiển thị chuyên nghiệp
            column_mapping = {
                'EmployeeID': 'Mã NV',
                'FullName': 'Họ Tên',
                'DepartmentName': 'Phòng Ban',
                'PositionName': 'Chức Vụ',
                'WorkDays': 'Ngày Công',
                'AbsentDays': 'Ngày Nghỉ',
                'BaseSalary': 'Lương Cơ Bản',
                'Bonus': 'Thưởng',
                'Deductions': 'Khấu Trừ',
                'NetSalary': 'Thực Nhận'
            }
            df = df.rename(columns=column_mapping)

            # 4. Ghi vào vùng nhớ (buffer) thay vì lưu file vật lý
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Payroll')
            
            output.seek(0)
            return {"status": "success", "data": output}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}