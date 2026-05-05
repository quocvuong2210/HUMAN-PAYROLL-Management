import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import MainLayout from './layouts/MainLayout';
import DashboardPage from './pages/DashboardPage';
import EmployeesPage from './pages/EmployeesPage';
import SalariesPage from './pages/SalariesPage';
import DepartmentsPage from './pages/DepartmentsPage';
import ProfilePage from './pages/ProfilePage';
import ReportsPage from './pages/ReportsPage';
import AlertsPage from './pages/AlertsPage';
import LoginPage from './pages/LoginPage';
import ProtectedRoute from './components/ProtectedRoute';
import UserPage from "./pages/UserPage";
import AccessLogsPage from "./pages/AccessLogsPage";
import ForbiddenPage from "./pages/ForbiddenPage";
import { ToastProvider } from './contexts/ToastContext';

/**
 * ============================================
 * PHÂN QUYỀN RÕ RÀNG - ROLE-BASED ACCESS CONTROL
 * ============================================
 * 
 * SUPER_ADMIN (admin):
 *   ✅ Tất cả trang
 *   ✅ Tạo user + phân quyền (UserPage)
 *   ✅ Xem access logs
 *   ✅ Quản lý departments, employees, salaries, reports
 * 
 * HR_MANAGER (hr_manager):
 *   ✅ Dashboard, Employees, Departments, Reports, Profile, Alerts
 *   ❌ Users (KHÔNG được tạo user)
 *   ❌ Access Logs (KHÔNG được xem)
 *   ❌ Salaries (KHÔNG được tính lương)
 * 
 * PAYROLL_ACCOUNTANT (accountant):
 *   ✅ Dashboard, Salaries, Reports, Profile
 *   ❌ Users, Access Logs, Departments
 *   ❌ Employees (chỉ xem, không quản lý)
 * 
 * EMPLOYEE (employee):
 *   ✅ Dashboard, Profile (chỉ của mình)
 *   ❌ Tất cả trang quản lý khác
 * 
 * ============================================
 */

function App() {
  return (
    <ToastProvider>
      <BrowserRouter>
        <Routes>
          {/* ===== PUBLIC ROUTES ===== */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/403" element={<ForbiddenPage />} />

          {/* ===== PROTECTED ROUTES ===== */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <MainLayout />
              </ProtectedRoute>
            }
          >
            {/* ===== ALL AUTHENTICATED USERS ===== */}
            <Route index element={<DashboardPage />} />
            <Route path="profile" element={<ProfilePage />} />
            <Route path="alerts" element={<AlertsPage />} />

            {/* ===== SUPER_ADMIN ONLY ===== */}
            {/* Chỉ SUPER_ADMIN được tạo user và phân quyền */}
            <Route
              path="users"
              element={
                <ProtectedRoute requiredRoles={['SUPER_ADMIN']}>
                  <UserPage />
                </ProtectedRoute>
              }
            />

            {/* Chỉ SUPER_ADMIN được xem access logs */}
            <Route
              path="access-logs"
              element={
                <ProtectedRoute requiredRoles={['SUPER_ADMIN']}>
                  <AccessLogsPage />
                </ProtectedRoute>
              }
            />

            {/* ===== SUPER_ADMIN + HR_MANAGER ===== */}
            {/* Quản lý nhân viên */}
            <Route
              path="employees"
              element={
                <ProtectedRoute requiredRoles={['SUPER_ADMIN', 'HR_MANAGER']}>
                  <EmployeesPage />
                </ProtectedRoute>
              }
            />

            {/* Quản lý phòng ban */}
            <Route
              path="departments"
              element={
                <ProtectedRoute requiredRoles={['SUPER_ADMIN', 'HR_MANAGER']}>
                  <DepartmentsPage />
                </ProtectedRoute>
              }
            />

            {/* ===== SUPER_ADMIN + PAYROLL_ACCOUNTANT ===== */}
            {/* Quản lý lương */}
            <Route
              path="salaries"
              element={
                <ProtectedRoute requiredRoles={['SUPER_ADMIN', 'PAYROLL_ACCOUNTANT']}>
                  <SalariesPage />
                </ProtectedRoute>
              }
            />

            {/* ===== SUPER_ADMIN + HR_MANAGER + PAYROLL_ACCOUNTANT ===== */}
            {/* Báo cáo */}
            <Route
              path="reports"
              element={
                <ProtectedRoute requiredRoles={['SUPER_ADMIN', 'HR_MANAGER', 'PAYROLL_ACCOUNTANT']}>
                  <ReportsPage />
                </ProtectedRoute>
              }
            />
          </Route>

          {/* ===== 404 - Redirect to home ===== */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </ToastProvider>
  );
}

export default App;
