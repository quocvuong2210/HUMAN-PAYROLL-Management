import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import {
  Cake, Award, AlertTriangle, Fingerprint,
  Loader2, X, Landmark, History, ChevronRight, Search, Info
} from 'lucide-react';
import { useOutletContext } from 'react-router-dom';
import { useToast } from '../contexts/ToastContext';

const API_BASE = `${import.meta.env.VITE_API_URL}/api/v1/alerts`;

export default function AlertsPage() {
  const { isDarkMode, language } = useOutletContext();
  const { showToast } = useToast();
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('birthday');
  const [data, setData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);

  const t = {
    vi: {
      title: "Hệ Thống Giám Sát",
      tabs: { birthday: "Sinh Nhật", anniversary: "Kỷ Niệm", salary: "Lương Bất Thường", attendance: "Nghỉ Quá Buổi" },
      cols: { name: "Nhân viên", dept: "Bộ phận", info: "Thông số" },
      noData: "Không có dữ liệu phù hợp", month: "Tháng", year: "Năm",
      detail: "Hồ sơ chi tiết", history: "Lịch sử công (3 tháng)", salary: "Diễn biến lương",
      status: "Trạng thái", position: "Vị trí", id: "Mã NV"
    },
    en: {
      title: "Monitoring System",
      tabs: { birthday: "Birthdays", anniversary: "Anniversary", salary: "Unusual Salary", attendance: "Absenteeism" },
      cols: { name: "Employee", dept: "Dept", info: "Metrics" },
      noData: "No matching data available", month: "Month", year: "Year",
      detail: "Detailed Profile", history: "Attendance (3 mos)", salary: "Salary Trends",
      status: "Status", position: "Position", id: "Emp ID"
    }
  }[language || 'vi'];

  const tabs = [
    { id: 'birthday', label: t.tabs.birthday, icon: Cake, endpoint: '/birthdays' },
    { id: 'anniversary', label: t.tabs.anniversary, icon: Award, endpoint: '/anniversaries' },
    { id: 'salary', label: t.tabs.salary, icon: AlertTriangle, endpoint: '/unusual-salaries' },
    { id: 'attendance', label: t.tabs.attendance, icon: Fingerprint, endpoint: '/absenteeism' },
  ];

  const formatDate = (dateString, type = 'month', lang = 'vi') => {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return "N/A";

    if (type === 'month') {
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const year = date.getFullYear();
      // Kiểm tra ngôn ngữ để trả về format phù hợp
      return lang === 'vi'
        ? `Tháng ${month}/${year}`
        : `Month ${month}/${year}`;
    }

    // Trả về ngày/tháng/năm tùy theo locale
    return date.toLocaleDateString(lang === 'vi' ? 'vi-VN' : 'en-US');
  };
  const fetchData = useCallback(async () => {
    setLoading(true);
    const currentTab = tabs.find(tab => tab.id === activeTab);
    if (!currentTab) return;

    const params = { month: selectedMonth };
    if (['salary', 'attendance'].includes(activeTab)) {
      params.year = selectedYear;
    }

    try {
      const response = await axios.get(`${API_BASE}${currentTab.endpoint}`, { params });
      setData(response.data.data || []);
    } catch (err) {
      setData([]);
    } finally {
      setLoading(false);
    }
  }, [activeTab, selectedMonth, selectedYear]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const fetchEmployeeDetail = async (id) => {
    setDetailLoading(true);
    setSelectedEmployee({ EmployeeID: id, FullName: "..." });
    try {
      const res = await axios.get(`${API_BASE}/employee/${id}`);
      setSelectedEmployee(res.data.data);
    } catch (err) {
      console.error(err);
      setSelectedEmployee(null);
    } finally { setDetailLoading(false); }
  };

  const filteredData = data.filter(item =>
    (item.FullName?.toLowerCase() || "").includes(searchTerm.toLowerCase()) ||
    (item.EmployeeID?.toString() || "").includes(searchTerm)
  );

  const formatCurrency = (val) => new Intl.NumberFormat('vi-VN').format(val || 0);

  return (
    <div className={`w-full h-full p-4 flex flex-col gap-4 transition-all duration-300 ${isDarkMode ? 'text-slate-300 bg-slate-950' : 'text-slate-800 bg-slate-50'}`}>

      {/* HEADER & FILTERS */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <h1 className="text-xl font-black tracking-tight uppercase border-l-4 border-blue-600 pl-3 leading-tight">{t.title}</h1>

          <div className={`flex items-center gap-1 p-1 rounded-lg border ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
            <select value={selectedMonth} onChange={(e) => setSelectedMonth(Number(e.target.value))} className="bg-transparent text-xs font-bold border-none focus:ring-0 py-0 h-7 cursor-pointer outline-none">
              {[...Array(12)].map((_, i) => <option key={i + 1} value={i + 1} className="text-black">{t.month} {i + 1}</option>)}
            </select>

            {['salary', 'attendance'].includes(activeTab) && (
              <select value={selectedYear} onChange={(e) => setSelectedYear(Number(e.target.value))} className={`bg-transparent text-xs font-bold border-l focus:ring-0 py-0 h-7 cursor-pointer ml-1 pl-1 outline-none ${isDarkMode ? 'border-slate-700' : 'border-slate-200'}`}>
                {[2024, 2025, 2026].map(y => <option key={y} value={y} className="text-black">{y}</option>)}
              </select>
            )}
          </div>
        </div>

        <div className={`relative flex items-center rounded-lg border w-full md:w-64 ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
          <Search size={14} className="absolute left-3 opacity-40" />
          <input
            type="text" placeholder="Tìm tên, mã NV..."
            className="bg-transparent border-none focus:ring-0 text-xs pl-10 pr-3 py-2 w-full"
            value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>
      {/* TAB SELECTOR: Dạng Gạch chân (Underline Tabs) */}
      <div className="flex gap-6 border-b border-gray-200 dark:border-slate-700 pb-4 overflow-x-auto no-scrollbar">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => { setActiveTab(tab.id); setSelectedEmployee(null); }}
            className={`pb-2 flex items-center gap-2 border-b-2 transition-all duration-200 shrink-0 ${activeTab === tab.id
              ? 'border-blue-500 text-blue-500 font-semibold'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
          >
            <tab.icon size={18} />
            {tab.label}
          </button>
        ))}
      </div>

      {/* MAIN CONTENT AREA */}
      <div className="flex-1 flex gap-4 min-h-0 overflow-hidden">

        {/* DATA TABLE */}
        <div className={`flex-1 rounded-xs border flex flex-col overflow-hidden ${isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
          <div className="flex-1  overflow-y-auto custom-scrollbar">
            <table className="w-full rounded-xs text-left border-collapse">
              <thead className={`sticky top-0 z-10 text-[10px] uppercase font-bold tracking-wider ${isDarkMode ? 'bg-slate-800 text-slate-400' : 'bg-slate-50 text-slate-500'}`}>
                <tr>
                  <th className="px-6 py-4">{t.cols.name}</th>
                  <th className="px-6 py-4">{t.cols.dept}</th>
                  <th className="px-6 py-4">{t.cols.info}</th>
                  <th className="px-6 py-4 text-right"></th>
                </tr>
              </thead>
              <tbody className={`divide-y ${isDarkMode ? 'divide-slate-800' : 'divide-slate-100'} text-xs`}>
                {loading ? (
                  <tr><td colSpan="4" className="py-24 text-center"><Loader2 className="animate-spin inline text-blue-500" size={32} /></td></tr>
                ) : filteredData.length > 0 ? (
                  filteredData.map((item, idx) => (
                    <tr
                      key={idx} onClick={() => fetchEmployeeDetail(item.EmployeeID)}
                      className={`hover:bg-blue-600/5 transition-all cursor-pointer group ${selectedEmployee?.EmployeeID === item.EmployeeID ? (isDarkMode ? 'bg-blue-600/10' : 'bg-blue-50') : ''}`}
                    >
                      <td className="px-6 py-2">
                        <div className="flex items-center gap-3">
                          <div className={`w-9 h-9 rounded-xl flex items-center justify-center font-black text-xs ${isDarkMode ? 'bg-slate-800 text-blue-400' : 'bg-blue-100 text-blue-600'}`}>
                            {item.FullName?.charAt(0)}
                          </div>
                          <div className="min-w-0">
                            <p className="font-bold text-sm truncate">{item.FullName}</p>
                            <p className="text-[10px] opacity-50 font-mono tracking-tighter">#{item.EmployeeID}</p>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-2 opacity-70 font-medium">{item.DepartmentName}</td>
                      <td className="px-6 py-2">
                        {activeTab === 'birthday' && (
                          <div className="flex flex-col">
                            <span className="text-blue-500 font-bold">Ngày {item.BirthDay}</span>
                            <span className="text-[10px] opacity-50 uppercase truncate max-w-[120px]">{item.PositionName}</span>
                          </div>
                        )}
                        {activeTab === 'anniversary' && (
                          <span className="bg-amber-500/10 text-amber-600 px-3 py-1 rounded-full font-black text-[10px] ring-1 ring-amber-500/20">{item.YearsActive} NĂM</span>
                        )}
                        {activeTab === 'salary' && (
                          <div className="flex flex-col">
                            <span className="text-rose-500 font-black font-mono text-sm">{formatCurrency(item.NetSalary)}</span>
                            <span className="text-[10px] text-red-400 italic truncate max-w-[150px]">{item.reason}</span>
                          </div>
                        )}
                        {activeTab === 'attendance' && (
                          <span className={`font-black text-[11px] px-2 py-0.5 rounded ${item.alert_level === 'CRITICAL' ? 'bg-red-500/10 text-red-500' : 'bg-orange-500/10 text-orange-500'}`}>
                            {item.display_msg}
                          </span>
                        )}
                      </td>
                      <td className="px-6 py-2 text-right">
                        <ChevronRight size={16} className={`transition-all opacity-0 group-hover:opacity-100 group-hover:translate-x-1 text-blue-500`} />
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr><td colSpan="4" className="py-24 text-center opacity-40 text-xs font-bold uppercase tracking-widest">{t.noData}</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* SIDEBAR DETAIL */}
        {selectedEmployee && (
          <div className={`w-96 flex flex-col rounded-2xl border animate-in slide-in-from-right-10 duration-300 shadow-2xl ${isDarkMode ? 'bg-[#0f172a] border-slate-800' : 'bg-white border-slate-200'}`}>
            <div className={`p-5 border-b flex justify-between items-center ${isDarkMode ? 'border-slate-800' : 'border-slate-100'}`}>
              <div className="flex items-center gap-2">
                <Info size={16} className="text-blue-500" />
                <h3 className="text-[11px] font-black uppercase tracking-widest text-blue-500">{t.detail}</h3>
              </div>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-8 custom-scrollbar">
              {detailLoading ? (
                <div className="flex flex-col items-center justify-center h-full opacity-40">
                  <Loader2 className="animate-spin mb-3 text-blue-500" size={32} />
                  <p className="text-xs font-bold uppercase tracking-tighter">Đang tải...</p>
                </div>
              ) : (
                <>
                  <div className="flex flex-col items-center text-center space-y-3">
                    <div className="w-20 h-20 bg-gradient-to-tr from-blue-600 to-cyan-400 rounded-3xl flex items-center justify-center text-white text-3xl font-black shadow-xl shadow-blue-500/20">
                      {selectedEmployee.FullName?.charAt(0)}
                    </div>
                    <div>
                      <h2 className="text-xl font-black uppercase leading-tight">{selectedEmployee.FullName}</h2>
                      <p className="text-xs opacity-50 font-mono mt-1">{t.id}: {selectedEmployee.EmployeeID}</p>
                    </div>
                    <span className="text-[10px] px-3 py-1 bg-green-500/10 text-green-500 rounded-full font-black uppercase ring-1 ring-green-500/20">
                      {selectedEmployee.Status || t.status}
                    </span>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className={`p-4 rounded-2xl border ${isDarkMode ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-100'}`}>
                      <p className="opacity-40 font-black text-[9px] mb-1 uppercase tracking-wider">{t.cols.dept}</p>
                      <p className="font-bold text-xs">{selectedEmployee.DepartmentName}</p>
                    </div>
                    <div className={`p-4 rounded-2xl border ${isDarkMode ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-100'}`}>
                      <p className="opacity-40 font-black text-[9px] mb-1 uppercase tracking-wider">{t.position}</p>
                      <p className="font-bold text-xs">{selectedEmployee.PositionName}</p>
                    </div>
                  </div>

                  <div className="space-y-6">
                    <section>
                      <h4 className="text-[10px] font-black uppercase text-slate-500 flex items-center gap-2 mb-4">
                        <History size={16} /> {t.history}
                      </h4>
                      <div className="space-y-3">
                        {selectedEmployee.attendance_history?.length > 0 ? selectedEmployee.attendance_history.slice(0, 3).map((a, i) => (
                          <div key={i} className={`p-4 rounded-xl flex items-center justify-between border ${isDarkMode ? 'bg-slate-800/30 border-slate-800 hover:bg-slate-800/50' : 'bg-white border-slate-100 shadow-sm hover:shadow-md'} transition-all`}>
                            <span className="text-xs font-black text-blue-500 uppercase">
                              {formatDate(a.AttendanceMonth, 'month', language)}
                            </span>
                            <div className="flex gap-6">
                              <div className="flex flex-col items-end"><span className="opacity-40 text-[8px] font-bold">CÔNG</span><span className="text-green-500 font-mono font-bold">{a.WorkDays}</span></div>
                              <div className="flex flex-col items-end"><span className="opacity-40 text-[8px] font-bold">NGHỈ</span><span className="text-rose-500 font-mono font-bold">{a.AbsentDays}</span></div>
                            </div>
                          </div>
                        )) : <p className="text-xs opacity-30 italic text-center">Không có dữ liệu công</p>}
                      </div>
                    </section>

                    <section>
                      <h4 className="text-[10px] font-black uppercase text-slate-500 flex items-center gap-2 mb-4">
                        <Landmark size={16} /> {t.salary}
                      </h4>
                      <div className="space-y-3">
                        {selectedEmployee.salary_history?.length > 0 ? selectedEmployee.salary_history.slice(0, 3).map((s, i) => (
                          <div key={i} className={`p-4 rounded-xl border ${isDarkMode ? 'bg-slate-800/30 border-slate-800 hover:bg-slate-800/50' : 'bg-white border-slate-100 shadow-sm hover:shadow-md'} transition-all`}>
                            <div className="flex justify-between items-center">
                              <span className="text-xs font-bold opacity-60">
                                {formatDate(s.SalaryMonth, 'month', language)}
                              </span>
                              <span className="font-black text-blue-500 font-mono">
                                {s.net_fmt || formatCurrency(s.NetSalary)} đ
                              </span>
                            </div>
                          </div>
                        )) : <p className="text-xs opacity-30 italic text-center">Không có dữ liệu lương</p>}
                      </div>
                    </section>
                  </div>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}