import React, { useState } from 'react';
import { 
  Home, Users, Building2, DollarSign, AlertTriangle, 
  BarChart3, User, Box, ChevronLeft, ChevronRight
} from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

// 1. Bộ từ điển dịch thuật
const translations = {
  vi: {
    system: "Hệ thống",
    overview: "Tổng quan",
    employees: "Nhân sự",
    structure: "Cơ cấu tổ chức",
    payroll: "Lương & Công",
    analysis: "Phân tích & Cá nhân",
    alerts: "Thông báo",
    reports: "Báo cáo số liệu",
    profile: "Hồ sơ cá nhân"
  },
  en: {
    system: "System",
    overview: "Overview",
    employees: "Employees",
    structure: "Organization",
    payroll: "Payroll",
    analysis: "Analysis & Personal",
    alerts: "Alerts",
    reports: "Reports",
    profile: "Profile"
  }
};

const NavItem = ({ icon: Icon, label, to, isCollapsed, isDarkMode }) => {
  const location = useLocation();
  const isActive = location.pathname === to || (to !== "/" && location.pathname.startsWith(to));

  return (
    <Link to={to}>
      <div
        className={`flex items-center gap-3 px-4 py-3 transition-all duration-200 mx-2 rounded-xl mb-1
        ${isActive 
          ? 'bg-indigo-600 text-white shadow-xs shadow-indigo-500/30' 
          : isDarkMode 
            ? 'text-slate-400 hover:text-slate-100 hover:bg-slate-800' 
            : 'text-slate-500 hover:text-indigo-600 hover:bg-indigo-50'
        }`}
      >
        <Icon size={20} className="min-w-[20px]" />
        {!isCollapsed && (
          <span className="text-sm font-semibold whitespace-nowrap">
            {label}
          </span>
        )}
      </div>
    </Link>
  );
};

export default function SideBar({ isDarkMode, language }) {
  const [isCollapsed, setIsCollapsed] = useState(false);
  
 
  const t = translations[language] || translations.vi;

  return (
    <div
      className={`relative h-full flex flex-col py-6 border-r transition-all duration-300 z-20
      ${isCollapsed ? 'w-20' : 'w-64'} 
      ${isDarkMode 
        ? 'bg-slate-950 border-slate-800 text-white' 
        : 'bg-white border-slate-100 text-slate-900'
      }`}
    >
      <style>{`
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
      `}</style>

      <button
  onClick={() => setIsCollapsed(!isCollapsed)}
  className={`absolute -right-3 top-12 rounded-full p-1.5 border-2 transition-all hover:scale-110 z-30

    bg-[#6366f1]  text-slate-900  border-[#6366f1]
    hover:bg-[#373ae0] hover:border-[#6366f1]`}
>
  {isCollapsed ? <ChevronRight size={14} strokeWidth={3} /> : <ChevronLeft size={14} strokeWidth={3} />}
</button>

      {/* Logo Section */}
      <div className={`px-6 mb-10 flex items-center gap-3 ${isCollapsed ? 'justify-center px-0' : ''}`}>
        <div className="w-9 h-9 bg-indigo-600 rounded-xl flex items-center justify-center text-white shadow-indigo-500/20 shadow-xs">
          <Box size={22} />
        </div>
        {!isCollapsed && (
          <span className="text-xl font-black tracking-tight bg-gradient-to-r from-indigo-600 to-violet-500 bg-clip-text text-transparent">
              Payroll & Human
          </span>
        )}
      </div>

      {/* Menu Navigation */}
      <div className="flex-1 overflow-y-auto no-scrollbar space-y-1">
        {!isCollapsed && (
          <p className={`px-8 text-[10px] font-bold uppercase tracking-widest mb-4 
            ${isDarkMode ? 'text-slate-600' : 'text-slate-400'}`}>
            {t.system}
          </p>
        )}

        <NavItem icon={Home} label={t.overview} to="/" isCollapsed={isCollapsed} isDarkMode={isDarkMode} />
        <NavItem icon={Users} label={t.employees} to="/employees" isCollapsed={isCollapsed} isDarkMode={isDarkMode} />
        <NavItem icon={Building2} label={t.structure} to="/departments" isCollapsed={isCollapsed} isDarkMode={isDarkMode} />
        <NavItem icon={DollarSign} label={t.payroll} to="/salaries" isCollapsed={isCollapsed} isDarkMode={isDarkMode} />

        {!isCollapsed && (
          <p className={`px-8 text-[10px] font-bold uppercase tracking-widest mt-8 mb-4 
            ${isDarkMode ? 'text-slate-600' : 'text-slate-400'}`}>
            {t.analysis}
          </p>
        )}

        <NavItem icon={AlertTriangle} label={t.alerts} to="/alerts" isCollapsed={isCollapsed} isDarkMode={isDarkMode} />
        <NavItem icon={BarChart3} label={t.reports} to="/reports" isCollapsed={isCollapsed} isDarkMode={isDarkMode} />
        <NavItem icon={User} label={t.profile} to="/profile" isCollapsed={isCollapsed} isDarkMode={isDarkMode} />
      </div>
    </div>
  );
}