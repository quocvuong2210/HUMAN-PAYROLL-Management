import MainLayout from './layouts/MainLayout'
import DashboardPage from './pages/DashboardPage'
import { BrowserRouter, Route, Routes } from "react-router-dom";
import EmployeesPage from './pages/EmployeesPage';
import SalariesPage from './pages/SalariesPage';
import DepartmentsPage from './pages/DepartmentsPage';
import ProfilePage from './pages/ProfilePage';
import ReportsPage from './pages/ReportsPage';
import AlertsPage from './pages/AlertsPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 👇 Layout cha */}
        <Route path="/" element={<MainLayout />}>
          
          {/* 👇 Các page con */}
          <Route index element={<DashboardPage />} />
          <Route path="departments" element={<DepartmentsPage />} />
          <Route path="employees" element={<EmployeesPage />} />
          <Route path="salaries" element={<SalariesPage />} />
          <Route path="reports" element={<ReportsPage />} />
          <Route path="profile" element={<ProfilePage />} />
          <Route path="alerts" element={<AlertsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App;