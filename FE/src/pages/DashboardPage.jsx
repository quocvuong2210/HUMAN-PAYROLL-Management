import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { Bar, Doughnut, Line, Pie } from 'react-chartjs-2';
import { 
  Chart as ChartJS, CategoryScale, LinearScale, BarElement, 
  PointElement, LineElement, Title, Tooltip, Legend, ArcElement,
  Filler 
} from 'chart.js';
import { AlertCircle, Users, TrendingUp, Calendar, Banknote } from 'lucide-react';
import { useOutletContext } from 'react-router-dom';
import { CheckCircle2 } from "lucide-react";
ChartJS.register(
  CategoryScale, LinearScale, BarElement, PointElement, 
  LineElement, ArcElement, Title, Tooltip, Legend, Filler
);

const API_BASE = `${import.meta.env.VITE_API_URL}/api/v1/dashboard`; 

export default function DashboardPage() {
  console.log("DashboardPage rendered with language:", API_BASE);
  const { isDarkMode, language } = useOutletContext();
  const [chartsData, setChartsData] = useState(null);
  const [summary, setSummary] = useState(null);
  const [alerts, setAlerts] = useState([]);

  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());

 
  const t = {
    vi: {
      loading: "Đang tải dữ liệu...",
      totalSalary: "Tổng lương chi trả",
      totalEmp: "Tổng nhân viên",
      unitEmp: "Nhân sự",
      org: "Cơ cấu tổ chức",
      unitDept: "Phòng ban",
      finance: "Biến động tài chính",
      bonus: "Thưởng",
      deduction: "Khấu trừ",
      month: "Tháng",
      year: "Năm",
      deptCost: "Chi phí bộ phận",
      yearDetail: `Chi tiết năm ${selectedYear}`,
      empDist: "Phân bổ nhân sự",
      alerts: "Cảnh báo",
      stable: "Hệ thống ổn định",
      totalCost: "Tổng chi",
      salaryLabel: "Lương"
    },
    en: {
      loading: "Loading data...",
      totalSalary: "Total Net Salary",
      totalEmp: "Total Employees",
      unitEmp: "Staffs",
      org: "Organization",
      unitDept: "Departments",
      finance: "Financial Fluctuations",
      bonus: "Bonus",
      deduction: "Deductions",
      month: "Month",
      year: "Year",
      deptCost: "Department Costs",
      yearDetail: `${selectedYear} Annual Detail`,
      empDist: "Staff Distribution",
      alerts: "Alerts",
      stable: "System Stable",
      totalCost: "Total",
      salaryLabel: "Salary"
    }
  }[language || 'vi'];
// 1. Thêm state lỗi
const [error, setError] = useState(null);

const fetchData = useCallback(async () => {
   
    setError(null);
    try {
        const params = `?month=${selectedMonth}&year=${selectedYear}`;
        const [resCharts, resSummary, resAlerts] = await Promise.all([
            axios.get(`${API_BASE}/charts${params}&view_mode=month`),
            axios.get(`${API_BASE}/summary`), 
            axios.get(`${API_BASE}/alerts${params}`)
        ]);
        
        // Kiểm tra dữ liệu trước khi set
        if (!resCharts.data?.charts || !resSummary.data?.data) {
            throw new Error("Dữ liệu trả về không đúng cấu trúc");
        }

        setChartsData(resCharts.data.charts);
        setSummary(resSummary.data.data); 
        console.log("Fetched alerts:", resSummary.data.data);
        setAlerts(resAlerts.data.data || []);
    } catch (err) {
        console.error("Lỗi:", err);
        setError(language === 'vi' ? "Không thể tải dữ liệu. Vui lòng thử lại!" : "Failed to load data.");
    } finally {
        
    }
}, [selectedMonth, selectedYear, language]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const chartTextColor = isDarkMode ? '#94a3b8' : '#64748b';

  // Hàm format tiền tệ (tự động đổi locale theo ngôn ngữ)
  const formatCurrency = (value) => {
    return new Intl.NumberFormat(language === 'vi' ? 'vi-VN' : 'en-US', { 
      style: 'currency', 
      currency: 'VND' 
    }).format(value);
  };

  return (
    <div className="w-full p-4 flex flex-col gap-4 overflow-hidden">
      { error ? (
      <div className="flex-1 flex flex-col items-center justify-center border-2 border-dashed border-rose-200 rounded-2xl bg-rose-50/30">
        <AlertCircle size={40} className="text-rose-500 mb-2" />
        <p className="text-rose-600 font-bold">{error}</p>
        <button 
          onClick={fetchData}
          className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg font-bold hover:bg-blue-700 transition-all"
        >
          {language === 'vi' ? 'Thử lại' : 'Retry'}
        </button>
      </div>
    ) :(
        <div className="flex-1 flex flex-col gap-4 min-h-0 overflow-hidden animate-in fade-in duration-500">
          
          {/* STATS CARDS */}
          <div className="grid grid-cols-4 gap-4 flex-shrink-0 ">
            <div className={`p-4 rounded-xl flex items-center justify-between transition-colors shadow-sm border ${isDarkMode ? 'bg-slate-950 border-slate-700' : 'bg-slate-50 border-slate-100'}`}>
              <div>
                <p className="text-[9px] font-bold text-slate-400 uppercase">{t.totalSalary}</p>
                <h3 className={`text-base font-black ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                  {formatCurrency(summary?.total_net_salary || 0)}
                </h3>
              </div>
              <div className="bg-blue-500/10 p-2 rounded-xl">
                <Banknote size={18} className="text-blue-500" />
              </div>
            </div>

            <div className={`p-4 rounded-xl flex items-center justify-between transition-colors shadow-sm border ${isDarkMode ? 'bg-slate-950 border-slate-700' : 'bg-slate-50 border-slate-100'}`}>
              <div>
                <p className="text-[9px] font-bold text-emerald-500 uppercase">{t.totalEmp}</p>
                <h3 className={`text-base font-black ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                  {summary?.total_employees || 0} <span className="text-[10px] text-slate-400 font-medium">{t.unitEmp}</span>
                </h3>
              </div>
              <div className="bg-emerald-500/10 p-2 rounded-xl">
                <Users size={18} className="text-emerald-500" />
              </div>
            </div>

            <div className={`p-4 rounded-xl flex items-center justify-between transition-colors shadow-sm border ${isDarkMode ? 'bg-slate-950 border-slate-700' : 'bg-slate-50 border-slate-100'}`}>
              <div>
                <p className="text-[9px] font-bold text-amber-500 uppercase">{t.org}</p>
                <h3 className={`text-base font-black ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                  {summary?.total_departments || 0} <span className="text-[10px] text-slate-400 font-medium">{t.unitDept}</span>
                </h3>
              </div>
              <div className="bg-amber-500/10 p-2 rounded-xl">
                <TrendingUp size={18} className="text-amber-500" />
              </div>
            </div>

            <div className={`p-4 rounded-xl transition-colors shadow-sm border ${isDarkMode ? 'bg-slate-950 border-slate-700' : 'bg-slate-50 border-slate-100'}`}>
              <p className="text-[9px] font-bold text-rose-500 uppercase mb-1">⚖️ {t.finance}</p>
              <div className="flex flex-col gap-0.5 text-[10px] font-bold">
                <div className="flex justify-between">
                  <span className="text-slate-400 font-medium">{t.bonus}:</span>
                  <span className="text-emerald-500">+{formatCurrency(summary?.total_bonus || 0)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400 font-medium">{t.deduction}:</span>
                  <span className="text-rose-500">-{formatCurrency(summary?.total_deductions || 0)}</span>
                </div>
              </div>
            </div>
          </div>

          {/* FILTER HEADER */}
          <div className="flex items-center justify-between flex-shrink-0">
            <div className={`flex items-center rounded-2xl p-1.5 shadow-md transition-all border ${
              isDarkMode ? 'bg-slate-950 border-slate-700' : 'bg-slate-50 border-slate-100'
            }`}>
              
              {/* Chọn Tháng */}
              <div className="flex items-center px-3 gap-2 group">
                <Calendar size={14} className="text-blue-500 group-hover:scale-110 transition-transform" />
                <select 
                  className={`bg-transparent border-none text-xs font-black focus:ring-0 cursor-pointer p-0 ${
                    isDarkMode ? 'text-slate-200' : 'text-slate-700'
                  }`}
                  value={selectedMonth}
                  onChange={(e) => setSelectedMonth(Number(e.target.value))}
                >
                  {[...Array(12)].map((_, i) => (
                    <option 
                      key={i+1} 
                      value={i+1} 
                      className={`${isDarkMode ? 'bg-slate-950 text-white' : 'bg-slate-50 text-slate-900'} font-sans py-2`}
                    >
                      {t.month} {i+1 < 10 ? `0${i+1}` : i+1}
                    </option>
                  ))}
                </select>
              </div>

              <div className={`h-4 w-[1.5px] mx-1 ${isDarkMode ? 'bg-slate-700' : 'bg-slate-200'}`}></div>

              {/* Chọn Năm */}
              <div className="flex items-center px-3 gap-1 group">
                <select 
                  className={`bg-transparent border-none text-xs font-black focus:ring-0 cursor-pointer p-0 ${
                    isDarkMode ? 'text-slate-200' : 'text-slate-700'
                  }`}
                  value={selectedYear}
                  onChange={(e) => setSelectedYear(Number(e.target.value))}
                >
                  {[2023, 2024, 2025, 2026].map(y => (
                    <option 
                      key={y} 
                      value={y} 
                      className={`${isDarkMode ? 'bg-slate-950 text-white' : 'bg-slate-50 text-slate-900'} font-sans py-2`}
                    >
                      {t.year} {y}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* CHARTS ROW 1 */}
          {/* CHARTS ROW 1 - Đặt chiều cao cố định để các biểu đồ không bị nhảy */}
<div className="grid grid-cols-2 gap-4 flex-shrink-0 h-[350px] min-h-0">
  
  {/* Bar Chart - Chi phí bộ phận */}
  <div className={`p-5 flex flex-col overflow-hidden transition-all duration-300 shadow-sm rounded-xl border ${
    isDarkMode ? 'bg-slate-950 border-slate-700' : 'bg-slate-50 border-slate-100'
  }`}>
    <h3 className="text-[11px] font-black text-slate-500 uppercase mb-4 flex items-center gap-2 tracking-wider">
      <TrendingUp size={14} className="text-blue-500"/> {t.deptCost}
    </h3>
    <div className="flex-1 min-h-0 relative">
      <Bar 
        key={`bar-${language}`}
        options={{ 
          responsive: true, 
          maintainAspectRatio: false, // Quan trọng: Để chart nhận chiều cao từ div cha
          animations: {
            y: {
              duration: 1000,
              easing: 'easeOutQuart',
              from: (ctx) => ctx.type === 'data' ? ctx.chart.scales.y.getPixelForValue(0) : undefined,
              delay: (ctx) => (ctx.type !== 'data' || ctx.yStarted) ? 0 : (ctx.yStarted = true, ctx.index * 100)
            }
          },
          plugins: { 
            legend: { display: false },
            tooltip: {
              backgroundColor: isDarkMode ? '#1e293b' : '#fff',
              titleColor: isDarkMode ? '#fff' : '#1e293b',
              bodyColor: isDarkMode ? '#cbd5e1' : '#475569',
              borderColor: '#6366f1',
              borderWidth: 1,
              cornerRadius: 8,
              padding: 10,
              callbacks: { label: (ctx) => ` ${t.totalCost}: ${formatCurrency(ctx.raw)}` }
            }
          },
          scales: { 
            y: { 
              beginAtZero: true, 
              grid: { color: isDarkMode ? 'rgba(255,255,255,0.05)' : '#f1f5f9' }, 
              ticks: { color: '#94a3b8', font: { size: 9 } } 
            }, 
            x: { grid: { display: false }, ticks: { color: '#94a3b8', font: { size: 9 } } } 
          }
        }}
        data={{
          labels: chartsData?.bar_chart?.map(d => (d.department || d.name).replace("Phòng ", "")) || [],
          datasets: [{ 
            data: chartsData?.bar_chart?.map(d => d.total) || [], 
            backgroundColor: (context) => {
              const ctx = context.chart.ctx;
              const gradient = ctx.createLinearGradient(0, 0, 0, 300);
              gradient.addColorStop(0, '#6366f1');
              gradient.addColorStop(1, 'rgba(99, 102, 241, 0.1)');
              return gradient;
            },
            borderRadius: 6,
            barThickness: 20,
          }]
        }} 
      />
    </div>
  </div>

  {/* Line Chart - Chi tiết năm */}
  <div className={`p-5 flex flex-col overflow-hidden transition-all duration-300 shadow-sm rounded-xl border ${
    isDarkMode ? 'bg-slate-950 border-slate-700' : 'bg-slate-50 border-slate-100'
  }`}>
    <h3 className="text-[11px] font-black text-slate-500 uppercase mb-4 flex items-center gap-2 tracking-wider">
        <TrendingUp size={14} className="text-emerald-500"/> {t.yearDetail}
    </h3>
    <div className="flex-1 min-h-0 relative">
      <Line 
        key={`line-${language}`}
        options={{ 
          responsive: true, 
          maintainAspectRatio: false,
          animations: {
            y: {
              duration: 1500,
              easing: 'easeOutQuart',
              from: (ctx) => ctx.type === 'data' ? ctx.chart.scales.y.getPixelForValue(0) : undefined
            }
          },
          interaction: { mode: 'index', intersect: false },
          plugins: { 
            legend: { display: false },
            tooltip: {
              backgroundColor: isDarkMode ? '#1e293b' : '#fff',
              borderColor: '#6366f1',
              borderWidth: 1,
              callbacks: { label: (ctx) => ` ${t.salaryLabel}: ${formatCurrency(ctx.raw)}` }
            }
          },
          scales: { 
            y: { 
              beginAtZero: true,
              grid: { color: isDarkMode ? 'rgba(255,255,255,0.05)' : '#f1f5f9' }, 
              ticks: { color: '#94a3b8', font: { size: 9 } } 
            }, 
            x: { grid: { display: false }, ticks: { color: '#94a3b8', font: { size: 9 } } } 
          }
        }}
        data={{
          labels: chartsData?.line_chart?.map(d => d.label || d.day || d.month) || [],
          datasets: [{ 
            data: chartsData?.line_chart?.map(d => d.salary || d.total) || [], 
            tension: 0.4, 
            borderColor: '#6366f1', 
            borderWidth: 3,
            fill: true,
            backgroundColor: (context) => {
              const ctx = context.chart.ctx;
              const gradient = ctx.createLinearGradient(0, 0, 0, 300);
              gradient.addColorStop(0, 'rgba(99, 102, 241, 0.2)');
              gradient.addColorStop(1, 'rgba(99, 102, 241, 0)');
              return gradient;
            },
            pointRadius: 2,
            pointHoverRadius: 5,
            pointBackgroundColor: '#6366f1',
          }]
        }}
      />
    </div>
  </div>
</div>

          {/* CHARTS ROW 2 (Pie & Alerts) */}
      
<div className="grid grid-cols-12 gap-4 h-[300px] flex-shrink-0 mb-4">
  
  {/* CỘT 1: BIỂU ĐỒ TRÒN (Pie Chart) */}
  <div className={`col-span-4 p-5 flex flex-col overflow-hidden transition-all duration-300 shadow-sm rounded-xl border ${
    isDarkMode ? 'bg-slate-950 border-slate-700' : 'bg-slate-50 border-slate-100'
  }`}>
    <h3 className="text-[11px] font-black text-slate-500 uppercase mb-4 tracking-wider">
      {t.empDist}
    </h3>
    
    {/* Container chứa Chart - Cần flex-1 và min-h-0 để Chart.js không bị tràn */}
    <div className="flex-1 relative flex items-center justify-center min-h-0">
      <Doughnut 
        key={`pie-${language}`}
        options={{ 
          maintainAspectRatio: false, 
          cutout: '70%', 
          layout: { padding: 5 },
          plugins: { 
            legend: { 
              position: 'bottom', 
              labels: { 
                color: chartTextColor, 
                boxWidth: 8,
                padding: 15,
                usePointStyle: true, 
                font: { size: 10, weight: '600' } 
              }
            },
            tooltip: {
              backgroundColor: isDarkMode ? '#1e293b' : '#fff',
              titleColor: isDarkMode ? '#fff' : '#1e293b',
              bodyColor: isDarkMode ? '#cbd5e1' : '#64748b',
              borderWidth: 1,
              borderColor: isDarkMode ? '#334155' : '#e2e8f0',
              padding: 12,
              cornerRadius: 8,
              callbacks: {
                label: (context) => {
                  const value = context.raw;
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = ((value / total) * 100).toFixed(1);
                  return ` ${context.label}: ${value} (${percentage}%)`;
                }
              }
            }
          }
        }}
        data={{
          labels: chartsData?.pie_chart?.map(s => s.status) || [],
          datasets: [{ 
            data: chartsData?.pie_chart?.map(s => s.value) || [], 
            backgroundColor: ['#6366f1', '#10b981', '#f59e0b', '#ef4444'],
            borderWidth: isDarkMode ? 3 : 2,
            borderColor: isDarkMode ? '#1e293b' : '#fff',
            hoverOffset: 15
          }]
        }} 
      />
      
      {/* Chỉ số tổng ở giữa biểu đồ */}
      <div className="absolute top-[40%] left-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col items-center justify-center pointer-events-none">
        <span className={`text-2xl font-black leading-none ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
          {chartsData?.pie_chart?.reduce((acc, curr) => acc + curr.value, 0) || 0}
        </span>
        <span className="text-[9px] text-slate-400 font-bold uppercase tracking-tighter mt-1">
          {t.unitEmp}
        </span>
      </div>
    </div>
  </div>

  {/* CỘT 2: DANH SÁCH CẢNH BÁO (Alerts List) */}
  <div className={`col-span-8 p-5 flex flex-col overflow-hidden transition-all duration-300 shadow-sm rounded-xl border ${
    isDarkMode ? 'bg-slate-950 border-slate-700' : 'bg-slate-50 border-slate-100'
  }`}>
    <div className="flex items-center justify-between mb-4">
      <h3 className="text-[11px] font-black text-rose-600 flex items-center gap-2 uppercase tracking-wider">
        <AlertCircle size={14} className="animate-pulse" /> {t.alerts} ({alerts?.length || 0})
      </h3>
      {alerts?.length > 0 && (
        <span className="text-[9px] font-bold text-slate-400 uppercase">Cuộn để xem thêm</span>
      )}
    </div>

    {/* Khu vực có thể cuộn (Scrollable Area) */}
    <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar">
      <div className="grid grid-cols-2 gap-3">
        {alerts && alerts.length > 0 ? (
          alerts.map((alert, i) => (
            <div 
              key={i} 
              className={`p-4 rounded-xl flex items-start gap-3 border transition-all hover:scale-[1.01] ${
                isDarkMode 
                  ? 'bg-slate-700/30 border-slate-600/50 hover:bg-slate-700/50' 
                  : 'bg-slate-50 border-slate-200/60 hover:bg-slate-50 hover:shadow-md'
              }`}
            >
              <div className="w-2 h-2 rounded-full bg-rose-500 mt-1.5 flex-shrink-0 shadow-[0_0_8px_rgba(244,63,94,0.6)]"></div>
              <div className="min-w-0">
                <p className="text-[10px] font-black text-rose-500 uppercase mb-0.5">
                  {alert.title || t.alerts}
                </p>
                <p className={`text-[12px] font-medium leading-relaxed ${
                  isDarkMode ? 'text-slate-300' : 'text-slate-600'
                }`}>
                  {alert.message || alert.content}
                </p>
                {alert.date && (
                  <p className="text-[9px] text-slate-400 mt-2 font-mono">{alert.date}</p>
                )}
              </div>
            </div>
          ))
        ) : (
          <div className="col-span-2 h-full flex flex-col items-center justify-center text-slate-400 py-10">
            <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mb-3">
               <CheckCircle2 size={24} className="text-emerald-500" />
            </div>
            <p className="text-[11px] font-bold uppercase tracking-widest">{t.stable}</p>
            <p className="text-[10px] mt-1 opacity-60">Mọi thứ đều đang hoạt động tốt</p>
          </div>
        )}
      </div>
    </div>
  </div>
</div>

        </div>
      )}
    </div>
  );
}