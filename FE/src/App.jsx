import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import MainLayout from './layouts/MainLayout';
import DashboardPage from './pages/DashboardPage';
import EmployeesPage from './pages/EmployeesPage';
import SalariesPage from './pages/SalariesPage';
import DepartmentsPage from './pages/DepartmentsPage';
import ProfilePage from './pages/ProfilePage';
import ReportsPage from './pages/ReportsPage';
import AlertsPage from './pages/AlertsPage';
import LoginPage from './pages/LoginPage'; // Trang đăng nhập
import ProtectedRoute from './components/ProtectedRoute'; // Thành phần bảo vệ
import { User } from "lucide-react";
import UserPage from "./pages/UserPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ROUTE CÔNG KHAI: Ai cũng vào được */}
        <Route path="/login" element={<LoginPage />} />

        {/* ROUTE BẢO VỆ: Chỉ dành cho người đã đăng nhập */}
        <Route 
          path="/" 
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
           
          }
        >
          {/* Tất cả page con ở đây đều được bảo vệ tự động */}
          <Route index element={<DashboardPage />} />
          <Route path="departments" element={<DepartmentsPage />} />
          <Route path="employees" element={<EmployeesPage />} />
          <Route path="salaries" element={<SalariesPage />} />
          <Route path="reports" element={<ReportsPage />} />
          <Route path="profile" element={<ProfilePage />} />
          <Route path="alerts" element={<AlertsPage />} />
          <Route path="user" element={<UserPage />} />
          <Route path="access-logs" element={<UserPage />} />
        </Route>

        {/* Xử lý khi gõ sai đường dẫn: Tự động về trang chủ (hoặc login) */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;