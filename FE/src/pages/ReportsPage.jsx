import React, { useState, useEffect, useCallback } from 'react'
import { useOutletContext } from 'react-router-dom'
import {
  BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts'
import {
  DollarSign, Users, TrendingUp, AlertCircle, Calendar,
  Building2, Award, FileText, UserCheck, Clock, Loader2,
  RefreshCw, Download, ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight,
  FileSpreadsheet, CheckCircle2
} from 'lucide-react'
import { exportReportExcel, exportReportPDF } from '../utils/exportHelpers'
import { useToast } from '../contexts/ToastContext'

const API_BASE = import.meta.env.VITE_API_URL

const translations = {
  vi: {
    title: 'Báo Cáo Tổng Hợp',
    totalSalary: 'Tổng Lương Chi Trả',
    totalEmployees: 'Tổng Nhân Viên',
    avgAttendance: 'Trung Bình Công',
    alerts: 'Cảnh Báo',
    salaryBydept: 'Lương Theo Bộ Phận',
    topDept: 'Bộ Phận Chi Phí Cao Nhất',
    bestEmployee: 'Nhân Viên Xuất Sắc',
    payrollDetail: 'Chi Tiết Lương',
    attendance: 'Chấm Công',
    attendanceRate: 'Tỉ Lệ Chấm Công',
    distribution: 'Phân Bố',
    byStatus: 'Theo Trạng Thái',
    byPosition: 'Theo Vị Trí',
    alertsTab: 'Cảnh Báo',
    noAlerts: 'Không có cảnh báo',
    people: 'người',
    workDays: 'Công',
    absentDays: 'Nghỉ',
    leaveDays: 'Phép',
    baseSalary: 'Lương CB',
    bonus: 'Thưởng',
    deductions: 'Khấu Trừ',
    netSalary: 'Thực Nhận',
    salaryTab: 'Lương & Chi Phí',
    staffs: 'nhân viên',
    perDay: 'VNĐ/ngày',
    refresh: 'Làm mới',
    loading: 'Đang tải...',
    name: 'Họ Tên',
    total: 'Tổng',
    results: 'kết quả',
    attendanceOverview: 'Tổng Quan Chấm Công',
    totalWorkDays: 'Tổng Ngày Công',
    totalAbsent: 'Tổng Nghỉ',
    totalLeave: 'Tổng Phép',
    systemAlerts: 'Cảnh Báo Hệ Thống',
    stable: 'Hệ Thống Ổn Định',
    noSystemAlerts: 'Mọi thứ đều đang hoạt động tốt'
  },
  en: {
    title: 'Reports Overview',
    totalSalary: 'Total Salary',
    totalEmployees: 'Total Employees',
    avgAttendance: 'Avg. Attendance',
    alerts: 'Alerts',
    salaryBydept: 'Salary by Department',
    topDept: 'Highest Cost Dept',
    bestEmployee: 'Best Employee',
    payrollDetail: 'Payroll Details',
    attendance: 'Attendance',
    attendanceRate: 'Attendance Rate',
    distribution: 'Distribution',
    byStatus: 'By Status',
    byPosition: 'By Position',
    alertsTab: 'Alerts',
    noAlerts: 'No alerts',
    people: 'people',
    workDays: 'Work',
    absentDays: 'Absent',
    leaveDays: 'Leave',
    baseSalary: 'Base',
    bonus: 'Bonus',
    deductions: 'Deduct',
    netSalary: 'Net',
    salaryTab: 'Salary & Costs',
    staffs: 'staffs',
    perDay: 'VND/day',
    refresh: 'Refresh',
    loading: 'Loading...',
    name: 'Name',
    total: 'Total',
    results: 'results',
    attendanceOverview: 'Attendance Overview',
    totalWorkDays: 'Total Work Days',
    totalAbsent: 'Total Absent',
    totalLeave: 'Total Leave',
    systemAlerts: 'System Alerts',
    stable: 'System Stable',
    noSystemAlerts: 'Everything is running smoothly'
  }
}

const CHART_COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#ec4899', '#84cc16']

export default function ReportsPage() {
  const { isDarkMode, language } = useOutletContext() || { isDarkMode: false, language: 'vi' }
  const lang = language || 'vi'
  const { showToast } = useToast()

  const [month, setMonth] = useState('2024-09')
  const [activeTab, setActiveTab] = useState('salary')
  const [isLoading, setIsLoading] = useState(false)

  const [salaryByDept, setSalaryByDept] = useState([])
  const [employeeDistribution, setEmployeeDistribution] = useState([])
  const [positionReport, setPositionReport] = useState([])
  const [attendanceReport, setAttendanceReport] = useState([])
  const [payrollDetail, setPayrollDetail] = useState([])
  const [alertReport, setAlertReport] = useState([])
  const [topDepartment, setTopDepartment] = useState([])
  const [bestEmployee, setBestEmployee] = useState([])
  const [dashboardAlerts, setDashboardAlerts] = useState([])

  const t = translations[lang]

  const fetchDashboardData = useCallback(async () => {
    setIsLoading(true)
    try {
      const [y, m] = month.split('-')
      const response = await fetch(
        `${API_BASE}/api/v1/reports/dashboard?month=${parseInt(m)}&year=${parseInt(y)}`
      )
      const result = await response.json()

      if (result.status === 'success' && result.data) {
        const data = result.data

        if (data.salaryByDept) {
          setSalaryByDept(data.salaryByDept.map(item => ({
            ...item,
            TotalSalary: parseFloat(item.TotalSalary)
          })))
        }

        if (data.employeeDistribution) setEmployeeDistribution(data.employeeDistribution)
        if (data.positionReport) setPositionReport(data.positionReport)

        if (data.attendanceReport) {
          const unique = data.attendanceReport.reduce((acc, curr) => {
            if (!acc.find(item => item.FullName === curr.FullName)) acc.push(curr)
            return acc
          }, [])
          setAttendanceReport(unique)
        }

        if (data.payrollDetail) {
          const unique = data.payrollDetail.reduce((acc, curr) => {
            if (!acc.find(item => item.FullName === curr.FullName)) {
              acc.push({
                ...curr,
                BaseSalary: parseFloat(curr.BaseSalary),
                Bonus: parseFloat(curr.Bonus),
                Deductions: parseFloat(curr.Deductions),
                NetSalary: parseFloat(curr.NetSalary)
              })
            }
            return acc
          }, [])
          setPayrollDetail(unique)
        }

        if (data.alertReport) {
          const unique = data.alertReport.reduce((acc, curr) => {
            if (!acc.find(item => item.FullName === curr.FullName)) {
              acc.push({ ...curr, NetSalary: parseFloat(curr.NetSalary) })
            }
            return acc
          }, [])
          setAlertReport(unique)
        }

        if (data.topDepartment?.length > 0) {
          setTopDepartment(data.topDepartment.map(item => ({
            ...item, TotalCost: parseFloat(item.TotalCost)
          })))
        }

        if (data.bestEmployee?.length > 0) {
          setBestEmployee(data.bestEmployee.map(item => ({
            ...item, SalaryPerDay: parseFloat(item.SalaryPerDay)
          })))
        }
      }

      // Fetch alerts from dashboard API (same as DashboardPage)
      try {
        const alertsResponse = await fetch(
          `${API_BASE}/api/v1/dashboard/alerts?month=${parseInt(m)}&year=${parseInt(y)}`
        )
        const alertsResult = await alertsResponse.json()
        setDashboardAlerts(alertsResult.data || [])
      } catch (alertErr) {
        console.error('Error fetching alerts:', alertErr)
        setDashboardAlerts([])
      }
    } catch (err) {
      console.error('Error fetching dashboard data:', err)
    } finally {
      setIsLoading(false)
    }
  }, [month])

  useEffect(() => {
    fetchDashboardData()
  }, [fetchDashboardData])

  const totalSalary = payrollDetail.reduce((sum, emp) => sum + (emp.NetSalary || 0), 0)
  const totalEmployees = employeeDistribution.reduce((sum, status) => sum + status.Total, 0)
  const avgAttendance = attendanceReport.length > 0
    ? (attendanceReport.reduce((sum, emp) => sum + emp.WorkDays, 0) / attendanceReport.length).toFixed(1)
    : '0'

  // Tong hop du lieu cham cong cho Pie Chart
  const totalWorkDays = attendanceReport.reduce((sum, emp) => sum + (emp.WorkDays || 0), 0)
  const totalAbsentDays = attendanceReport.reduce((sum, emp) => sum + (emp.AbsentDays || 0), 0)
  const totalLeaveDays = attendanceReport.reduce((sum, emp) => sum + (emp.LeaveDays || 0), 0)

  const attendancePieData = [
    { name: t.totalWorkDays, value: totalWorkDays, color: '#10b981' },
    { name: t.totalAbsent, value: totalAbsentDays, color: '#ef4444' },
    { name: t.totalLeave, value: totalLeaveDays, color: '#f59e0b' }
  ]

  const formatCurrency = (value) => {
    if (!value && value !== 0) return '0 VND'
    return new Intl.NumberFormat(lang === 'vi' ? 'vi-VN' : 'en-US', {
      style: 'currency',
      currency: 'VND',
      maximumFractionDigits: 0
    }).format(value)
  }

  // --- TOAST HELPER ---
  // Toast is now handled by useToast hook

  // --- EXPORT FUNCTIONS ---
  const handleExportExcel = async () => {
    setIsLoading(true);

    let reportData = {};

    if (activeTab === 'salary') {
      reportData = {
        report_type: 'salary',
        headers: [t.name, t.baseSalary, t.bonus, t.deductions, t.netSalary],
        data: payrollDetail.map(emp => [
          emp.FullName,
          emp.BaseSalary,
          emp.Bonus,
          emp.Deductions,
          emp.NetSalary
        ])
      };
    } else if (activeTab === 'attendance') {
      reportData = {
        report_type: 'attendance',
        headers: [t.name, t.workDays, t.absentDays, t.leaveDays],
        data: attendanceReport.map(emp => [
          emp.FullName,
          emp.WorkDays,
          emp.AbsentDays,
          emp.LeaveDays
        ])
      };
    } else if (activeTab === 'distribution') {
      reportData = {
        report_type: 'distribution',
        headers: ['Status', 'Total'],
        data: employeeDistribution.map(item => [item.Status, item.Total])
      };
    } else if (activeTab === 'alerts') {
      reportData = {
        report_type: 'alerts',
        headers: [t.name, t.absentDays, t.netSalary],
        data: alertReport.map(emp => [
          emp.FullName,
          emp.AbsentDays,
          emp.NetSalary
        ])
      };
    }

    await exportReportExcel(reportData, showToast);
    setIsLoading(false);
  };

  const handleExportPDF = async () => {
    setIsLoading(true);

    let reportData = {};

    if (activeTab === 'salary') {
      reportData = {
        report_type: 'salary',
        headers: [t.name, t.baseSalary, t.bonus, t.deductions, t.netSalary],
        data: payrollDetail.map(emp => [
          emp.FullName,
          emp.BaseSalary,
          emp.Bonus,
          emp.Deductions,
          emp.NetSalary
        ])
      };
    } else if (activeTab === 'attendance') {
      reportData = {
        report_type: 'attendance',
        headers: [t.name, t.workDays, t.absentDays, t.leaveDays],
        data: attendanceReport.map(emp => [
          emp.FullName,
          emp.WorkDays,
          emp.AbsentDays,
          emp.LeaveDays
        ])
      };
    } else if (activeTab === 'distribution') {
      reportData = {
        report_type: 'distribution',
        headers: ['Status', 'Total'],
        data: employeeDistribution.map(item => [item.Status, item.Total])
      };
    } else if (activeTab === 'alerts') {
      reportData = {
        report_type: 'alerts',
        headers: [t.name, t.absentDays, t.netSalary],
        data: alertReport.map(emp => [
          emp.FullName,
          emp.AbsentDays,
          emp.NetSalary
        ])
      };
    }

    await exportReportPDF(reportData, showToast);
    setIsLoading(false);
  };

  const tabs = [
    { id: 'salary', label: t.salaryTab, icon: DollarSign },
    { id: 'attendance', label: t.attendance, icon: Clock },
    { id: 'distribution', label: t.distribution, icon: Users },
    { id: 'alerts', label: t.alertsTab, icon: AlertCircle }
  ]

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className={`px-3 py-2 rounded-lg shadow-lg border text-xs ${isDarkMode ? 'bg-slate-800 border-slate-700 text-white' : 'bg-white border-slate-200 text-slate-800'
          }`}>
          <p className="font-bold mb-1">{label || payload[0]?.name}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color || entry.payload?.color }} className="font-medium">
              {entry.name}: {typeof entry.value === 'number' && entry.value > 10000
                ? formatCurrency(entry.value)
                : entry.value}
            </p>
          ))}
        </div>
      )
    }
    return null
  }

  return (
    <div className={`p-6 flex flex-col gap-6 ${isDarkMode ? 'text-slate-300' : 'text-slate-800'}`}>

      {/* Header Tabs */}
      <div className="flex items-center justify-between border-b border-gray-200 dark:border-slate-700 pb-4">
        <div className="flex gap-6">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`pb-2 flex items-center gap-2 border-b-2 transition-all duration-200 ${activeTab === tab.id
                  ? 'border-blue-500 text-blue-500 font-semibold'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
              >
                <Icon size={18} /> {tab.label}
              </button>
            )
          })}
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={fetchDashboardData}
            disabled={isLoading}
            className="text-xs px-3 py-1.5 bg-blue-600/10 text-blue-600 rounded-lg flex items-center gap-2 hover:bg-blue-600/20 disabled:opacity-50"
          >
            <RefreshCw size={14} className={isLoading ? 'animate-spin' : ''} />
            {t.refresh}
          </button>

          {/* Export Buttons */}
          <button
            onClick={handleExportExcel}
            disabled={isLoading}
            className="text-xs px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-400 text-white rounded-lg flex items-center gap-2 transition-all"
            title="Xuất Excel"
          >
            <FileSpreadsheet size={14} />
            Excel
          </button>
          <button
            onClick={handleExportPDF}
            disabled={isLoading}
            className="text-xs px-3 py-1.5 bg-rose-600 hover:bg-rose-700 disabled:bg-rose-400 text-white rounded-lg flex items-center gap-2 transition-all"
            title="Xuất PDF"
          >
            <FileText size={14} />
            PDF
          </button>
        </div>
      </div>

      {/* Filter Bar */}
      <div className={`grid grid-cols-2 md:grid-cols-6 gap-3 p-4 rounded-xl border ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
        }`}>
        <input
          type="month"
          value={month}
          onChange={(e) => setMonth(e.target.value)}
          className="px-3 py-2 rounded-lg border text-sm bg-transparent"
        />
      </div>

      {/* Tab Content */}
      <div className={`flex-1 border overflow-hidden rounded-xl ${isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200'
        }`}>

        {/* Loading */}
        {isLoading && (
          <div className="text-center p-10">
            <Loader2 className="animate-spin inline text-blue-500" size={32} />
            <p className="mt-2 text-sm opacity-60">{t.loading}</p>
          </div>
        )}

        {/* SALARY TAB */}
        {!isLoading && activeTab === 'salary' && (
          <div className="p-5 flex flex-col gap-6">
            {/* Salary by Department Chart */}
            <div>
              <h3 className="text-xs font-black text-slate-500 uppercase mb-4 flex items-center gap-2 tracking-wider">
                <TrendingUp size={14} className="text-blue-500" />
                {t.salaryBydept}
              </h3>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={salaryByDept} margin={{ top: 10, right: 10, left: 10, bottom: 60 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke={isDarkMode ? '#334155' : '#e2e8f0'} />
                    <XAxis
                      dataKey="DepartmentName"
                      tick={{ fontSize: 9, fill: isDarkMode ? '#94a3b8' : '#64748b' }}
                      angle={-45}
                      textAnchor="end"
                      height={80}
                      interval={0}
                    />
                    <YAxis
                      tick={{ fontSize: 10, fill: isDarkMode ? '#94a3b8' : '#64748b' }}
                      tickFormatter={(value) => `${(value / 1000000).toFixed(0)}M`}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Bar dataKey="TotalSalary" name={t.netSalary} fill="#3b82f6" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Top Dept & Best Employee */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Top Department */}
              <div className={`p-4 rounded-xl border ${isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-slate-50 border-slate-200'}`}>
                <h3 className="text-xs font-black text-slate-500 uppercase mb-3 flex items-center gap-2">
                  <Building2 size={14} className="text-amber-500" />
                  {t.topDept}
                </h3>
                {topDepartment[0] && (
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center">
                      <Building2 size={20} className="text-white" />
                    </div>
                    <div>
                      <p className={`text-lg font-black ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                        {topDepartment[0].DepartmentName}
                      </p>
                      <p className="text-amber-500 text-sm font-bold">
                        {formatCurrency(topDepartment[0].TotalCost)}
                      </p>
                    </div>
                  </div>
                )}
              </div>

              {/* Best Employee */}
              <div className={`p-4 rounded-xl border ${isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-slate-50 border-slate-200'}`}>
                <h3 className="text-xs font-black text-slate-500 uppercase mb-3 flex items-center gap-2">
                  <Award size={14} className="text-emerald-500" />
                  {t.bestEmployee}
                </h3>
                {bestEmployee[0] && (
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-400 to-teal-500 flex items-center justify-center">
                      <Award size={20} className="text-white" />
                    </div>
                    <div>
                      <p className={`text-lg font-black ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                        {bestEmployee[0].FullName}
                      </p>
                      <p className="text-emerald-500 text-sm font-bold">
                        {formatCurrency(bestEmployee[0].SalaryPerDay)} {t.perDay}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Payroll Detail Table */}
            <div>
              <h3 className="text-xs font-black text-slate-500 uppercase mb-3 flex items-center gap-2">
                <FileText size={14} className="text-blue-500" />
                {t.payrollDetail}
              </h3>
              <table className="w-full text-sm">
                <thead className={isDarkMode ? 'bg-slate-800' : 'bg-slate-100'}>
                  <tr>
                    <th className="p-4 text-left">{t.name}</th>
                    <th className="p-4 text-right">{t.baseSalary}</th>
                    <th className="p-4 text-right">{t.bonus}</th>
                    <th className="p-4 text-right">{t.deductions}</th>
                    <th className="p-4 text-right">{t.netSalary}</th>
                  </tr>
                </thead>
                <tbody className={`divide-y ${isDarkMode ? 'divide-slate-800' : 'divide-slate-100'} text-xs`}>
                  {payrollDetail.map((emp, i) => (
                    <tr key={i} className="hover:bg-slate-500/5">
                      <td className="p-4 font-semibold">{emp.FullName}</td>
                      <td className="p-4 text-right">{formatCurrency(emp.BaseSalary)}</td>
                      <td className="p-4 text-right text-emerald-500">+{formatCurrency(emp.Bonus)}</td>
                      <td className="p-4 text-right text-rose-500">-{formatCurrency(emp.Deductions)}</td>
                      <td className="p-4 text-right font-bold text-blue-600">{formatCurrency(emp.NetSalary)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ATTENDANCE TAB */}
        {!isLoading && activeTab === 'attendance' && (
          <div className="p-5 flex flex-col gap-6">
            {/* Attendance Pie Chart */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-xs font-black text-slate-500 uppercase mb-4 flex items-center gap-2 tracking-wider">
                  <Clock size={14} className="text-blue-500" />
                  {t.attendanceOverview}
                </h3>
                <div className="h-72">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={attendancePieData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={100}
                        paddingAngle={3}
                        dataKey="value"
                        nameKey="name"
                        label={({ name, value }) => `${name}: ${value}`}
                        labelLine={false}
                      >
                        {attendancePieData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip content={<CustomTooltip />} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
                <div className="flex flex-wrap justify-center gap-4 mt-4">
                  {attendancePieData.map((item, i) => (
                    <div key={i} className="flex items-center gap-2 text-xs">
                      <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                      <span className={isDarkMode ? 'text-slate-300' : 'text-slate-600'}>
                        {item.name}: <span className="font-bold">{item.value}</span>
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Attendance Rate */}
              <div>
                <h3 className="text-xs font-black text-slate-500 uppercase mb-4 flex items-center gap-2 tracking-wider">
                  <TrendingUp size={14} className="text-emerald-500" />
                  {t.attendanceRate}
                </h3>
                <div className="flex flex-col gap-3 max-h-80 overflow-y-auto">
                  {attendanceReport.map((emp, i) => {
                    const rate = ((emp.WorkDays / 23) * 100).toFixed(0)
                    return (
                      <div key={i} className="flex items-center gap-4">
                        <div className={`w-28 text-xs font-bold truncate ${isDarkMode ? 'text-slate-300' : 'text-slate-700'}`}>
                          {emp.FullName}
                        </div>
                        <div className="flex-1">
                          <div className={`h-2 rounded-full ${isDarkMode ? 'bg-slate-700' : 'bg-slate-200'}`}>
                            <div
                              className={`h-full rounded-full transition-all ${rate >= 90 ? 'bg-emerald-500' : rate >= 70 ? 'bg-amber-500' : 'bg-rose-500'
                                }`}
                              style={{ width: `${Math.min(rate, 100)}%` }}
                            />
                          </div>
                        </div>
                        <div className={`w-12 text-right text-xs font-black ${rate >= 90 ? 'text-emerald-500' : rate >= 70 ? 'text-amber-500' : 'text-rose-500'
                          }`}>
                          {rate}%
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            </div>

            {/* Attendance Detail Table */}
            <div>
              <h3 className="text-xs font-black text-slate-500 uppercase mb-3 flex items-center gap-2">
                <UserCheck size={14} className="text-blue-500" />
                {t.attendance}
              </h3>
              <table className="w-full text-sm">
                <thead className={isDarkMode ? 'bg-slate-800' : 'bg-slate-100'}>
                  <tr>
                    <th className="p-4 text-left">{t.name}</th>
                    <th className="p-4 text-center">{t.workDays}</th>
                    <th className="p-4 text-center">{t.absentDays}</th>
                    <th className="p-4 text-center">{t.leaveDays}</th>
                  </tr>
                </thead>
                <tbody className={`divide-y ${isDarkMode ? 'divide-slate-800' : 'divide-slate-100'} text-xs`}>
                  {attendanceReport.map((emp, i) => (
                    <tr key={i} className="hover:bg-slate-500/5">
                      <td className="p-4 font-semibold">{emp.FullName}</td>
                      <td className="p-4 text-center">
                        <span className="px-2 py-1 rounded-full bg-emerald-500/20 text-emerald-500 font-bold">
                          {emp.WorkDays}
                        </span>
                      </td>
                      <td className="p-4 text-center">
                        <span className="px-2 py-1 rounded-full bg-rose-500/20 text-rose-500 font-bold">
                          {emp.AbsentDays}
                        </span>
                      </td>
                      <td className="p-4 text-center">
                        <span className="px-2 py-1 rounded-full bg-amber-500/20 text-amber-500 font-bold">
                          {emp.LeaveDays}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* DISTRIBUTION TAB */}
        {!isLoading && activeTab === 'distribution' && (
          <div className="p-5 grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Status Distribution */}
            <div>
              <h3 className="text-xs font-black text-slate-500 uppercase mb-4 flex items-center gap-2 tracking-wider">
                <Users size={14} className="text-blue-500" />
                {t.byStatus}
              </h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={employeeDistribution}
                      cx="50%"
                      cy="50%"
                      innerRadius={50}
                      outerRadius={80}
                      paddingAngle={3}
                      dataKey="Total"
                      nameKey="Status"
                      label={({ Status, Total }) => `${Status}: ${Total}`}
                      labelLine={false}
                    >
                      {employeeDistribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip content={<CustomTooltip />} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="flex flex-wrap justify-center gap-3 mt-4">
                {employeeDistribution.map((item, i) => (
                  <div key={i} className="flex items-center gap-1.5 text-xs">
                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: CHART_COLORS[i % CHART_COLORS.length] }} />
                    <span className={isDarkMode ? 'text-slate-300' : 'text-slate-600'}>{item.Status}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Position Distribution */}
            <div>
              <h3 className="text-xs font-black text-slate-500 uppercase mb-4 flex items-center gap-2 tracking-wider">
                <Users size={14} className="text-amber-500" />
                {t.byPosition}
              </h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={positionReport} layout="vertical" margin={{ top: 5, right: 30, left: 100, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke={isDarkMode ? '#334155' : '#e2e8f0'} />
                    <XAxis type="number" tick={{ fontSize: 10, fill: isDarkMode ? '#94a3b8' : '#64748b' }} />
                    <YAxis
                      dataKey="PositionName"
                      type="category"
                      tick={{ fontSize: 9, fill: isDarkMode ? '#94a3b8' : '#64748b' }}
                      width={95}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Bar dataKey="Total" name={t.people} fill="#f59e0b" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        {/* ALERTS TAB */}
        {!isLoading && activeTab === 'alerts' && (
          <div className="p-5 space-y-6">
            {/* System Alerts Section - Only in Alerts Tab */}
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xs font-black text-rose-600 flex items-center gap-2 uppercase tracking-wider">
                  <AlertCircle size={14} className="animate-pulse" /> {t.systemAlerts} ({dashboardAlerts?.length || 0})
                </h3>
                {dashboardAlerts?.length > 0 && (
                  <span className="text-[9px] font-bold text-slate-400 uppercase">Cuộn để xem thêm</span>
                )}
              </div>

              <div className="max-h-[200px] overflow-y-auto pr-2 custom-scrollbar">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  {dashboardAlerts && dashboardAlerts.length > 0 ? (
                    dashboardAlerts.map((alert, i) => (
                      <div
                        key={i}
                        className={`p-4 rounded-xl flex items-start gap-3 border transition-all hover:scale-[1.01] ${isDarkMode
                          ? 'bg-slate-800/30 border-slate-700/50 hover:bg-slate-800/50'
                          : 'bg-slate-50 border-slate-200/60 hover:bg-slate-100 hover:shadow-md'
                          }`}
                      >
                        <div className="w-2 h-2 rounded-full bg-rose-500 mt-1.5 flex-shrink-0 shadow-[0_0_8px_rgba(244,63,94,0.6)]"></div>
                        <div className="min-w-0">
                          <p className="text-[10px] font-black text-rose-500 uppercase mb-0.5">
                            {alert.title || t.systemAlerts}
                          </p>
                          <p className={`text-[12px] font-medium leading-relaxed ${isDarkMode ? 'text-slate-300' : 'text-slate-600'
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
                    <div className="col-span-full flex flex-col items-center justify-center text-slate-400 py-8">
                      <div className="w-12 h-12 rounded-full bg-emerald-500/10 flex items-center justify-center mb-3">
                        <CheckCircle2 size={24} className="text-emerald-500" />
                      </div>
                      <p className="text-[11px] font-bold uppercase tracking-widest">{t.stable}</p>
                      <p className="text-[10px] mt-1 opacity-60">{t.noSystemAlerts}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Alert Report Table */}
            <div>
              <h3 className="text-xs font-black text-slate-500 uppercase mb-4 flex items-center gap-2 tracking-wider">
                <AlertCircle size={14} className="text-rose-500" />
                {t.alertsTab}
              </h3>

              {alertReport.length === 0 ? (
                <div className={`text-center py-12 rounded-xl border-2 border-dashed ${isDarkMode ? 'border-slate-700' : 'border-slate-200'
                  }`}>
                  <AlertCircle size={48} className="mx-auto text-emerald-500 mb-4" />
                  <p className={`text-lg font-bold ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                    {t.noAlerts}
                  </p>
                </div>
              ) : (
                <table className="w-full text-sm">
                  <thead className={isDarkMode ? 'bg-slate-800' : 'bg-slate-100'}>
                    <tr>
                      <th className="p-4 text-left">{t.name}</th>
                      <th className="p-4 text-center">{t.absentDays}</th>
                      <th className="p-4 text-right">{t.netSalary}</th>
                    </tr>
                  </thead>
                  <tbody className={`divide-y ${isDarkMode ? 'divide-slate-800' : 'divide-slate-100'} text-xs`}>
                    {alertReport.map((emp, i) => (
                      <tr key={i} className="hover:bg-rose-500/5">
                        <td className="p-4 font-semibold">{emp.FullName}</td>
                        <td className="p-4 text-center">
                          <span className="px-2 py-1 rounded-full bg-rose-500/20 text-rose-500 font-bold">
                            {emp.AbsentDays}
                          </span>
                        </td>
                        <td className="p-4 text-right font-bold text-rose-600">{formatCurrency(emp.NetSalary)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className={`px-6 py-3 border rounded-xl flex items-center justify-between ${isDarkMode ? 'border-slate-800 bg-slate-900/60' : 'border-slate-100 bg-slate-50/50'
        }`}>
        <span className="text-[10px] font-bold uppercase opacity-50">
          {t.total}: {payrollDetail.length} {t.results}
        </span>
      </div>
    </div>
  )
}
