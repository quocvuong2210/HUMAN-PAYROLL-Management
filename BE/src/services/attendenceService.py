from src.models.attendenceModel import AttendanceModel
from datetime import datetime

class AttendanceService:
    def __init__(self):
        self.model = AttendanceModel()

    # --- 1. REPORT (Có hỗ trợ phân trang) ---
   # --- 1. REPORT (Có hỗ trợ phân trang và SẮP XẾP) ---
    def get_attendance_report(self, filters):
        page = int(filters.get('page', 1))
        limit = int(filters.get('limit', 10))
        
        # Lấy tham số sắp xếp
        sort_by = filters.get('sort_by', 'FullName')
        sort_order = filters.get('sort_order', 'ASC')
        
        return self.model.get_full_attendance_list(
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

    # --- 2. ADD ---
    def record_employee_attendance(self, data):
        # (Giữ nguyên logic cũ vì phần này không cần phân trang)
        try:
            if not data or 'EmployeeID' not in data:
                return {"status": "error", "message": "Thiếu EmployeeID"}

            emp_id = data['EmployeeID']
            month = data.get('AttendanceMonth', datetime.now().strftime('%Y-%m-01'))

            if not self.model.check_employee_exists(emp_id):
                return {"status": "error", "message": "Nhân viên không tồn tại"}

            if self.model.check_attendance_exists(emp_id, month):
                return {"status": "error", "message": "Đã chấm công tháng này"}

            work = int(data.get('WorkDays', 0))
            absent = int(data.get('AbsentDays', 0))
            leave = int(data.get('LeaveDays', 0))

            if work + absent + leave > 31:
                return {"status": "error", "message": "Tổng ngày > 31"}

            data['AttendanceMonth'] = month
            self.model.insert_attendance(data)

            return {"status": "success", "message": "Thêm thành công"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # --- 3. MISSING (Thêm phân trang tương tự Report nếu cần) ---
    def list_missing_attendance(self, filters):
        page = int(filters.get('page', 1))
        limit = int(filters.get('limit', 10))
        
        return self.model.get_missing_attendance(
            month=filters.get('month'),
            name=filters.get('name'),
            dept_id=filters.get('dept_id'),
            page=page,
            limit=limit
        )

    # --- 4. UPDATE ---
    def update_attendance(self, attendance_id, data):
        if not data:
            return {"status": "error", "message": "Thiếu dữ liệu"}

        affected = self.model.update_attendance(attendance_id, data)

        if affected > 0:
            return {"status": "success", "message": "Cập nhật thành công"}
        return {"status": "error", "message": "Không tìm thấy bản ghi"}