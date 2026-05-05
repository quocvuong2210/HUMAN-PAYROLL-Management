/**
 * Export Helper Functions
 * Các hàm hỗ trợ xuất Excel và PDF
 */

/**
 * Xuất nhân viên ra Excel
 */
export const exportEmployeesExcel = async (filters, showToast) => {
    try {
        console.log('🔄 Starting Excel export...');

        // Lấy token
        const token = localStorage.getItem('accessToken') ||
            localStorage.getItem('access_token') ||
            localStorage.getItem('token');

        if (!token) {
            console.error('❌ No token found');
            showToast?.('Vui lòng đăng nhập lại', 'error');
            return false;
        }

        console.log('✅ Token found:', token.substring(0, 20) + '...');

        // Tạo query params
        const queryParams = new URLSearchParams({
            name: filters.name || '',
            dept_id: filters.dept_id || '',
            pos_id: filters.pos_id || '',
            status: filters.status || '',
            gender: filters.gender || '',
            start_date: filters.start_date || '',
            end_date: filters.end_date || ''
        }).toString();

        const url = `${import.meta.env.VITE_API_URL}/api/v1/export/employees/excel?${queryParams}`;
        console.log('📡 Calling API:', url);

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        console.log('📥 Response status:', response.status);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Export failed:', errorText);
            showToast?.(`Lỗi: ${response.status} - ${response.statusText}`, 'error');
            return false;
        }

        // Download file
        const blob = await response.blob();
        console.log('📦 Blob size:', blob.size, 'bytes');

        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `Danh_sach_nhan_vien_${new Date().toISOString().split('T')[0]}.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        document.body.removeChild(a);

        console.log('✅ Excel exported successfully');
        showToast?.('Xuất Excel thành công!', 'success');
        return true;
    } catch (err) {
        console.error('❌ Export Excel error:', err);
        showToast?.('Lỗi xuất Excel: ' + err.message, 'error');
        return false;
    }
};

/**
 * Xuất nhân viên ra PDF
 */
export const exportEmployeesPDF = async (filters, showToast) => {
    try {
        console.log('🔄 Starting PDF export...');

        const token = localStorage.getItem('accessToken') ||
            localStorage.getItem('access_token') ||
            localStorage.getItem('token');

        if (!token) {
            console.error('❌ No token found');
            showToast?.('Vui lòng đăng nhập lại', 'error');
            return false;
        }

        const queryParams = new URLSearchParams({
            name: filters.name || '',
            dept_id: filters.dept_id || '',
            pos_id: filters.pos_id || '',
            status: filters.status || '',
            gender: filters.gender || '',
            start_date: filters.start_date || '',
            end_date: filters.end_date || ''
        }).toString();

        const url = `${import.meta.env.VITE_API_URL}/api/v1/export/employees/pdf?${queryParams}`;
        console.log('📡 Calling API:', url);

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        console.log('📥 Response status:', response.status);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Export failed:', errorText);
            showToast?.(`Lỗi: ${response.status} - ${response.statusText}`, 'error');
            return false;
        }

        const blob = await response.blob();
        console.log('📦 Blob size:', blob.size, 'bytes');

        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `Danh_sach_nhan_vien_${new Date().toISOString().split('T')[0]}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        document.body.removeChild(a);

        console.log('✅ PDF exported successfully');
        showToast?.('Xuất PDF thành công!', 'success');
        return true;
    } catch (err) {
        console.error('❌ Export PDF error:', err);
        showToast?.('Lỗi xuất PDF: ' + err.message, 'error');
        return false;
    }
};

/**
 * Xuất báo cáo ra Excel
 */
export const exportReportExcel = async (reportData, showToast) => {
    try {
        console.log('🔄 Starting Report Excel export...');
        console.log('📊 Report data:', reportData);

        const token = localStorage.getItem('accessToken') ||
            localStorage.getItem('access_token') ||
            localStorage.getItem('token');

        if (!token) {
            console.error('❌ No token found');
            showToast?.('Vui lòng đăng nhập lại', 'error');
            return false;
        }

        const url = `${import.meta.env.VITE_API_URL}/api/v1/export/report/excel`;
        console.log('📡 Calling API:', url);

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(reportData)
        });

        console.log('📥 Response status:', response.status);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Export failed:', errorText);
            showToast?.(`Lỗi: ${response.status} - ${response.statusText}`, 'error');
            return false;
        }

        const blob = await response.blob();
        console.log('📦 Blob size:', blob.size, 'bytes');

        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `Bao_cao_${reportData.report_type}_${new Date().toISOString().split('T')[0]}.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        document.body.removeChild(a);

        console.log('✅ Report Excel exported successfully');
        showToast?.('Xuất Excel thành công!', 'success');
        return true;
    } catch (err) {
        console.error('❌ Export Report Excel error:', err);
        showToast?.('Lỗi xuất Excel: ' + err.message, 'error');
        return false;
    }
};

/**
 * Xuất báo cáo ra PDF
 */
export const exportReportPDF = async (reportData, showToast) => {
    try {
        console.log('🔄 Starting Report PDF export...');
        console.log('📊 Report data:', reportData);

        const token = localStorage.getItem('accessToken') ||
            localStorage.getItem('access_token') ||
            localStorage.getItem('token');

        if (!token) {
            console.error('❌ No token found');
            showToast?.('Vui lòng đăng nhập lại', 'error');
            return false;
        }

        const url = `${import.meta.env.VITE_API_URL}/api/v1/export/report/pdf`;
        console.log('📡 Calling API:', url);

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(reportData)
        });

        console.log('📥 Response status:', response.status);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Export failed:', errorText);
            showToast?.(`Lỗi: ${response.status} - ${response.statusText}`, 'error');
            return false;
        }

        const blob = await response.blob();
        console.log('📦 Blob size:', blob.size, 'bytes');

        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `Bao_cao_${reportData.report_type}_${new Date().toISOString().split('T')[0]}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        document.body.removeChild(a);

        console.log('✅ Report PDF exported successfully');
        showToast?.('Xuất PDF thành công!', 'success');
        return true;
    } catch (err) {
        console.error('❌ Export Report PDF error:', err);
        showToast?.('Lỗi xuất PDF: ' + err.message, 'error');
        return false;
    }
};


// ==================== SALARY EXPORT ====================

/**
 * Xuất bảng lương ra Excel
 */
export const exportSalaryExcel = async (filters, showToast) => {
    try {
        console.log('🔄 Starting Salary Excel export...');

        const token = localStorage.getItem('accessToken') ||
            localStorage.getItem('access_token') ||
            localStorage.getItem('token');

        if (!token) {
            showToast?.('Vui lòng đăng nhập lại', 'error');
            return false;
        }

        const queryParams = new URLSearchParams({
            month: filters.month || '',
            name: filters.name || '',
            dept_id: filters.dept_id || '',
            pos_id: filters.pos_id || '',
            status: filters.status || ''
        }).toString();

        const url = `${import.meta.env.VITE_API_URL}/api/v1/export/salary/excel?${queryParams}`;
        console.log('📡 Calling API:', url);

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        console.log('📥 Response status:', response.status);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Export failed:', errorText);
            showToast?.(`Lỗi: ${response.status} - ${response.statusText}`, 'error');
            return false;
        }

        const blob = await response.blob();
        console.log('📦 Blob size:', blob.size, 'bytes');

        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = `Bang_luong_${new Date().toISOString().slice(0, 10)}.xlsx`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);

        console.log('✅ Salary Excel exported successfully');
        showToast?.('Xuất Excel thành công!', 'success');
        return true;

    } catch (error) {
        console.error('❌ Export Salary Excel error:', error);
        showToast?.(`Lỗi xuất Excel: ${error.message}`, 'error');
        return false;
    }
};

/**
 * Xuất bảng lương ra PDF
 */
export const exportSalaryPDF = async (filters, showToast) => {
    try {
        console.log('🔄 Starting Salary PDF export...');

        const token = localStorage.getItem('accessToken') ||
            localStorage.getItem('access_token') ||
            localStorage.getItem('token');

        if (!token) {
            showToast?.('Vui lòng đăng nhập lại', 'error');
            return false;
        }

        const queryParams = new URLSearchParams({
            month: filters.month || '',
            name: filters.name || '',
            dept_id: filters.dept_id || '',
            pos_id: filters.pos_id || '',
            status: filters.status || ''
        }).toString();

        const url = `${import.meta.env.VITE_API_URL}/api/v1/export/salary/pdf?${queryParams}`;
        console.log('📡 Calling API:', url);

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        console.log('📥 Response status:', response.status);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Export failed:', errorText);
            showToast?.(`Lỗi: ${response.status} - ${response.statusText}`, 'error');
            return false;
        }

        const blob = await response.blob();
        console.log('📦 Blob size:', blob.size, 'bytes');

        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = `Bang_luong_${new Date().toISOString().slice(0, 10)}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);

        console.log('✅ Salary PDF exported successfully');
        showToast?.('Xuất PDF thành công!', 'success');
        return true;

    } catch (error) {
        console.error('❌ Export Salary PDF error:', error);
        showToast?.(`Lỗi xuất PDF: ${error.message}`, 'error');
        return false;
    }
};

// ==================== ATTENDANCE EXPORT ====================

/**
 * Xuất bảng chấm công ra Excel
 */
export const exportAttendanceExcel = async (filters, showToast) => {
    try {
        console.log('🔄 Starting Attendance Excel export...');

        const token = localStorage.getItem('accessToken') ||
            localStorage.getItem('access_token') ||
            localStorage.getItem('token');

        if (!token) {
            showToast?.('Vui lòng đăng nhập lại', 'error');
            return false;
        }

        const queryParams = new URLSearchParams({
            month: filters.month || '',
            name: filters.name || '',
            dept_id: filters.dept_id || '',
            pos_id: filters.pos_id || '',
            status: filters.status || ''
        }).toString();

        const url = `${import.meta.env.VITE_API_URL}/api/v1/export/attendance/excel?${queryParams}`;
        console.log('📡 Calling API:', url);

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        console.log('📥 Response status:', response.status);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Export failed:', errorText);
            showToast?.(`Lỗi: ${response.status} - ${response.statusText}`, 'error');
            return false;
        }

        const blob = await response.blob();
        console.log('📦 Blob size:', blob.size, 'bytes');

        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = `Bang_cham_cong_${new Date().toISOString().slice(0, 10)}.xlsx`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);

        console.log('✅ Attendance Excel exported successfully');
        showToast?.('Xuất Excel thành công!', 'success');
        return true;

    } catch (error) {
        console.error('❌ Export Attendance Excel error:', error);
        showToast?.(`Lỗi xuất Excel: ${error.message}`, 'error');
        return false;
    }
};

/**
 * Xuất bảng chấm công ra PDF
 */
export const exportAttendancePDF = async (filters, showToast) => {
    try {
        console.log('🔄 Starting Attendance PDF export...');

        const token = localStorage.getItem('accessToken') ||
            localStorage.getItem('access_token') ||
            localStorage.getItem('token');

        if (!token) {
            showToast?.('Vui lòng đăng nhập lại', 'error');
            return false;
        }

        const queryParams = new URLSearchParams({
            month: filters.month || '',
            name: filters.name || '',
            dept_id: filters.dept_id || '',
            pos_id: filters.pos_id || '',
            status: filters.status || ''
        }).toString();

        const url = `${import.meta.env.VITE_API_URL}/api/v1/export/attendance/pdf?${queryParams}`;
        console.log('📡 Calling API:', url);

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        console.log('📥 Response status:', response.status);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Export failed:', errorText);
            showToast?.(`Lỗi: ${response.status} - ${response.statusText}`, 'error');
            return false;
        }

        const blob = await response.blob();
        console.log('📦 Blob size:', blob.size, 'bytes');

        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = `Bang_cham_cong_${new Date().toISOString().slice(0, 10)}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);

        console.log('✅ Attendance PDF exported successfully');
        showToast?.('Xuất PDF thành công!', 'success');
        return true;

    } catch (error) {
        console.error('❌ Export Attendance PDF error:', error);
        showToast?.(`Lỗi xuất PDF: ${error.message}`, 'error');
        return false;
    }
};
