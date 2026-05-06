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
import AccessLogsPage from "./pages/AccessLogsPage";
import ForbiddenPage from "./pages/ForbiddenPage";
import DividendsPage from "./pages/DividendsPage";
import { ToastProvider } from './contexts/ToastContext';


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

            <Route index element={<DashboardPage />} />
            <Route path="profile" element={<ProfilePage />} />
            <Route path="alerts" element={<AlertsPage />} />

            <Route
              path="access-logs"
              element={
                <ProtectedRoute requiredRoles={['SUPER_ADMIN']}>
                  <AccessLogsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="employees"
              element={
                <ProtectedRoute requiredRoles={['SUPER_ADMIN', 'HR_MANAGER']}>
                  <EmployeesPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="departments"
              element={
                <ProtectedRoute requiredRoles={['SUPER_ADMIN', 'HR_MANAGER']}>
                  <DepartmentsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="salaries"
              element={
                <ProtectedRoute requiredRoles={['SUPER_ADMIN', 'PAYROLL_ACCOUNTANT']}>
                  <SalariesPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="reports"
              element={
                <ProtectedRoute requiredRoles={['SUPER_ADMIN', 'HR_MANAGER', 'PAYROLL_ACCOUNTANT']}>
                  <ReportsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="dividends"
              element={
                <ProtectedRoute requiredRoles={['SUPER_ADMIN', 'HR_MANAGER', 'PAYROLL_ACCOUNTANT']}>
                  <DividendsPage />
                </ProtectedRoute>
              }
            />
          </Route>


          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </ToastProvider>
  );
}

export default App;
