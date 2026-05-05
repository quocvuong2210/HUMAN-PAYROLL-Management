import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Edit3, Save, X, Search, Loader2, ChevronLeft, ChevronRight,
  Clock, DollarSign, ChevronsLeft, ChevronsRight, FileDown, ArrowUpDown,
  FileSpreadsheet, FileText
} from 'lucide-react';
import { useOutletContext } from 'react-router-dom';
import * as XLSX from 'xlsx';
import jsPDF from 'jspdf';
import 'jspdf-autotable';
import {
  exportSalaryExcel,
  exportSalaryPDF,
  exportAttendanceExcel,
  exportAttendancePDF
} from '../utils/exportHelpers';
import { useToast } from '../contexts/ToastContext';

const API_BASE = import.meta.env.VITE_API_URL;

export default function HRManagementPage() {
  const { isDarkMode, language } = useOutletContext();
  const { showToast } = useToast();
  const [activeTab, setActiveTab] = useState('attendance');

  const [data, setData] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [positions, setPositions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [limit] = useState(10);
  const [totalRecords, setTotalRecords] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [month, setMonth] = useState(new Date().toISOString().slice(0, 7));
  const [status, setStatus] = useState('');
  const [deptId, setDeptId] = useState('');
  const [posId, setPosId] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState({});

  const [sortConfig, setSortConfig] = useState({ key: 'FullName', direction: 'ASC' });
  const [actionLoading, setActionLoading] = useState(false);

  const totalPages = Math.ceil(totalRecords / limit) || 1;

  // Danh sách cột không cho phép click sắp xếp
  const nonSortableCols = ['ID', 'Bộ phận / Vị trí', 'Dept / Pos', 'Trạng thái', 'Status', ''];

  const t = {
    vi: {
      attendance: "Chấm công", salary: "Quản lý lương",
      allStatus: "Tất cả trạng thái", allDept: "Tất cả bộ phận", allPos: "Tất cả vị trí",
      search: "Tìm tên nhân viên...", total: "Tổng", results: "kết quả", errorSave: "Lỗi lưu dữ liệu!",
      attendanceStatus: { recorded: "Đã chấm", pending: "Chưa chấm" },
      salaryStatus: { calculated: "Đã tính", pending: "Chưa tính" },
      cols: {
        attendance: ['ID', 'Nhân viên', 'Bộ phận / Vị trí', 'Trạng thái', 'Công', 'Nghỉ', 'Phép', ''],
        salary: ['ID', 'Nhân viên', 'Bộ phận / Vị trí', 'Trạng thái', 'Lương CB', 'Thưởng', 'Khấu trừ', 'Thực nhận', '']
      }
    },
    en: {
      attendance: "Attendance", salary: "Salary Management",
      allStatus: "All status", allDept: "All departments", allPos: "All positions",
      search: "Search employee name...", total: "Total", results: "results", errorSave: "Error saving data!",
      attendanceStatus: { recorded: "Recorded", pending: "Pending" },
      salaryStatus: { calculated: "Calculated", pending: "Pending" },
      cols: {
        attendance: ['ID', 'Employee', 'Dept / Pos', 'Status', 'Work', 'Absent', 'Leave', ''],
        salary: ['ID', 'Employee', 'Dept / Pos', 'Status', 'Base', 'Bonus', 'Deduct', 'Net', '']
      }
    }
  }[language || 'vi'];

  const columnMapping = {
    'ID': 'EmployeeID', 'Nhân viên': 'FullName', 'Employee': 'FullName',
    'Bộ phận / Vị trí': 'DepartmentName', 'Dept / Pos': 'DepartmentName',
    'Công': 'WorkDays', 'Work': 'WorkDays',
    'Nghỉ': 'AbsentDays', 'Absent': 'AbsentDays',
    'Phép': 'LeaveDays', 'Leave': 'LeaveDays',
    'Lương CB': 'BaseSalary', 'Base': 'BaseSalary',
    'Thưởng': 'Bonus', 'Bonus': 'Bonus',
    'Khấu trừ': 'Deductions', 'Deduct': 'Deductions',
    'Thực nhận': 'NetSalary', 'Net': 'NetSalary'
  };

  const handleSort = (colLabel) => {
    if (nonSortableCols.includes(colLabel)) return;
    const key = columnMapping[colLabel] || 'FullName';
    const direction = (sortConfig.key === key && sortConfig.direction === 'ASC') ? 'DESC' : 'ASC';
    setSortConfig({ key, direction });
    setPage(1);
  };

  const handleExportExcel = async () => {
    setActionLoading(true);
    if (activeTab === 'attendance') {
      await exportAttendanceExcel({
        month: `${month}-01`,
        name: searchTerm,
        dept_id: deptId,
        pos_id: posId,
        status
      }, showToast);
    } else {
      await exportSalaryExcel({
        month: `${month}-01`,
        name: searchTerm,
        dept_id: deptId,
        pos_id: posId,
        status
      }, showToast);
    }
    setActionLoading(false);
  };

  const handleExportPDF = async () => {
    setActionLoading(true);
    if (activeTab === 'attendance') {
      await exportAttendancePDF({
        month: `${month}-01`,
        name: searchTerm,
        dept_id: deptId,
        pos_id: posId,
        status
      }, showToast);
    } else {
      await exportSalaryPDF({
        month: `${month}-01`,
        name: searchTerm,
        dept_id: deptId,
        pos_id: posId,
        status
      }, showToast);
    }
    setActionLoading(false);
  };

  const fetchData = async () => {
    setLoading(true);
    const endpoint = activeTab === 'attendance' ? '/api/v1/attendance/' : '/api/v1/salary/';
    try {
      const res = await axios.get(`${API_BASE}${endpoint}`, {
        params: { month: `${month}-01`, name: searchTerm, dept_id: deptId, pos_id: posId, status, page, limit, sort_by: sortConfig.key, sort_order: sortConfig.direction }
      });
      setData(res.data.data.data || []);
      setTotalRecords(res.data.data.total_records || 0);
    } catch (err) { console.error(err); } finally { setLoading(false); }
  };

  useEffect(() => {
    const fetchMetadata = async () => {
      try {
        const [d, p] = await Promise.all([axios.get(`${API_BASE}/api/v1/departments/`), axios.get(`${API_BASE}/api/v1/positions/`)]);
        setDepartments(d.data.data || []);
        setPositions(p.data.data || []);
      } catch (err) { console.error(err); }
    };
    fetchMetadata();
  }, []);

  useEffect(() => {
    setEditingId(null);
    fetchData();
  }, [activeTab, month, status, page, deptId, posId, searchTerm, sortConfig]);

  const handleSave = async (item) => {
    try {
      if (activeTab === 'salary') {
        if (item.SalaryID) await axios.put(`${API_BASE}/api/v1/salary/${item.SalaryID}`, form);
        else await axios.post(`${API_BASE}/api/v1/salary/process`, { EmployeeID: item.EmployeeID, SalaryMonth: `${month}-01`, ...form });
      } else {
        if (item.isRecorded === 1) await axios.put(`${API_BASE}/api/v1/attendance/${item.AttendanceID}`, form);
        else await axios.post(`${API_BASE}/api/v1/attendance/`, { EmployeeID: item.EmployeeID, AttendanceMonth: `${month}-01`, ...form });
      }
      setEditingId(null);
      fetchData();
    } catch (err) { alert(t.errorSave); }
  };

  return (
    <div className={`p-6 flex flex-col gap-6 ${isDarkMode ? 'text-slate-300' : 'text-slate-800'}`}>
      {/* Header Tabs */}
      <div className="flex items-center justify-between border-b border-gray-200 dark:border-slate-700 pb-4">
        <div className="flex gap-6">
          {/* Tab Chấm công */}
          <button
            onClick={() => { setActiveTab('attendance'); setPage(1); }}
            className={`pb-2 flex items-center gap-2 border-b-2 transition-all duration-200 ${activeTab === 'attendance'
              ? 'border-blue-500 text-blue-500 font-semibold'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
          >
            <Clock size={18} /> {t.attendance}
          </button>

          {/* Tab Lương */}
          <button
            onClick={() => { setActiveTab('salary'); setPage(1); }}
            className={`pb-2 flex items-center gap-2 border-b-2 transition-all duration-200 ${activeTab === 'salary'
              ? 'border-blue-500 text-blue-500 font-semibold'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
          >
            <DollarSign size={18} /> {t.salary}
          </button>
        </div>

        {/* Export Buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleExportExcel}
            disabled={actionLoading || data.length === 0}
            className="text-xs px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-400 text-white rounded-lg flex items-center gap-2 transition-all"
          >
            {actionLoading ? <Loader2 size={14} className="animate-spin" /> : <FileSpreadsheet size={14} />}
            Excel
          </button>
          <button
            onClick={handleExportPDF}
            disabled={actionLoading || data.length === 0}
            className="text-xs px-3 py-1.5 bg-rose-600 hover:bg-rose-700 disabled:bg-rose-400 text-white rounded-lg flex items-center gap-2 transition-all"
          >
            {actionLoading ? <Loader2 size={14} className="animate-spin" /> : <FileText size={14} />}
            PDF
          </button>
        </div>
      </div>



      {/* Filters */}
      <div className={`grid grid-cols-2 md:grid-cols-6 gap-3 p-4 rounded-xl border ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'}`}>
        <input type="month" value={month} onChange={(e) => setMonth(e.target.value)} className="px-3 py-2 rounded-lg border text-sm bg-transparent" />
        <select value={status} onChange={(e) => setStatus(e.target.value)} className="px-3 py-2 rounded-lg border text-sm bg-transparent">
          <option value="">{t.allStatus}</option>
          {activeTab === 'attendance' ? <><option value="1">{t.attendanceStatus.recorded}</option><option value="0">{t.attendanceStatus.pending}</option></> : <><option value="calculated">{t.salaryStatus.calculated}</option><option value="pending">{t.salaryStatus.pending}</option></>}
        </select>
        <select value={deptId} onChange={(e) => setDeptId(e.target.value)} className="px-3 py-2 rounded-lg border text-sm bg-transparent"><option value="">{t.allDept}</option>{departments.map(d => <option key={d.DepartmentID} value={d.DepartmentID}>{d.DepartmentName}</option>)}</select>
        <select value={posId} onChange={(e) => setPosId(e.target.value)} className="px-3 py-2 rounded-lg border text-sm bg-transparent"><option value="">{t.allPos}</option>{positions.map(p => <option key={p.PositionID} value={p.PositionID}>{p.PositionName}</option>)}</select>
        <div className="md:col-span-2 flex items-center gap-2 border rounded-lg px-3">
          <Search size={16} /><input placeholder={t.search} value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} className="w-full bg-transparent outline-none text-sm py-2" />
        </div>
      </div>

      {/* Table */}
      <div className={`flex-1 border overflow-hidden rounded-xs ${isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200'}`}>
        <table className="w-full text-sm">
          <thead className={isDarkMode ? 'bg-slate-800' : 'bg-slate-100'}>
            <tr>
              {t.cols[activeTab].map(col => (
                <th key={col} className={`p-4 text-left ${!nonSortableCols.includes(col) ? 'cursor-pointer hover:opacity-70' : ''}`} onClick={() => handleSort(col)}>
                  <div className="flex items-center gap-1">
                    {col} {!nonSortableCols.includes(col) && <ArrowUpDown size={12} className={sortConfig.key === columnMapping[col] ? 'text-blue-500' : ''} />}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className={`divide-y ${isDarkMode ? 'divide-slate-800' : 'divide-slate-100'} text-xs`}>
            {loading ? <tr><td colSpan="9" className="text-center p-10"><Loader2 className="animate-spin inline" /></td></tr> :
              data.map((item) => (
                <tr key={item.EmployeeID} className="border-t hover:bg-slate-500/5">
                  <td className="p-4">{item.EmployeeID}</td>
                  <td className="font-semibold">{item.FullName}</td>
                  <td>
                    <div className="flex flex-col">
                      <span className="font-semibold text-blue-500">{item.DepartmentName}</span>
                      <span className="text-[10px] opacity-50 font-medium">{item.PositionName}</span>
                    </div>
                  </td>
                  <td>
                    <span className={`px-2 py-1 rounded-full text-[10px] ${item.isRecorded || item.salaryStatus === 'calculated' ? 'bg-emerald-500/20 text-emerald-500' : 'bg-amber-500/20 text-amber-500'}`}>
                      {activeTab === 'attendance' ? (item.isRecorded ? t.attendanceStatus.recorded : t.attendanceStatus.pending) : (item.salaryStatus === 'calculated' ? t.salaryStatus.calculated : t.salaryStatus.pending)}
                    </span>
                  </td>
                  {activeTab === 'attendance' ? (
                    <>
                      {['WorkDays', 'AbsentDays', 'LeaveDays'].map(f => (
                        <td key={f}>{editingId === item.EmployeeID ? <input type="number" defaultValue={item[f]} onChange={(e) => setForm({ ...form, [f]: e.target.value })} className="w-12 border rounded bg-transparent" /> : (item[f] || 0)}</td>
                      ))}
                    </>
                  ) : (
                    <>
                      {['BaseSalary', 'Bonus', 'Deductions'].map(f => (
                        <td key={f}>{editingId === item.EmployeeID ? <input type="number" defaultValue={item[f]} onChange={(e) => setForm({ ...form, [f]: e.target.value })} className="w-20 border rounded bg-transparent" /> : (item[f] || 0).toLocaleString()}</td>
                      ))}
                      <td className="font-bold text-emerald-600">{parseFloat(item.NetSalary || 0).toLocaleString()}</td>
                    </>
                  )}
                  <td>
                    {editingId === item.EmployeeID ?
                      <div className="flex gap-2"><button onClick={() => handleSave(item)}><Save size={16} /></button><button onClick={() => setEditingId(null)}><X size={16} /></button></div>
                      : <button onClick={() => { setEditingId(item.EmployeeID); setForm(activeTab === 'salary' ? { BaseSalary: item.BaseSalary, Bonus: item.Bonus, Deductions: item.Deductions } : { WorkDays: item.WorkDays, AbsentDays: item.AbsentDays, LeaveDays: item.LeaveDays }); }}><Edit3 size={16} /></button>
                    }
                  </td>
                </tr>
              ))}
          </tbody>
        </table>

        {/* Pagination */}
        <div className={`px-6 py-3 border-t flex items-center justify-between gap-4 ${isDarkMode ? 'border-slate-800 bg-slate-900/60' : 'border-slate-100 bg-slate-50/50'}`}>
          <span className="text-[10px] font-bold uppercase opacity-50">{t.total}: {totalRecords} {t.results}</span>
          <div className="flex items-center gap-1">
            <button disabled={page === 1} onClick={() => setPage(1)} className="p-2 rounded-lg hover:bg-blue-500/10 disabled:opacity-20 transition-all"><ChevronsLeft size={16} /></button>
            <button disabled={page === 1} onClick={() => setPage(p => p - 1)} className="p-2 rounded-lg hover:bg-blue-500/10 disabled:opacity-20 transition-all"><ChevronLeft size={16} /></button>
            <div className="flex items-center px-4 gap-2">
              <span className="w-8 h-8 flex items-center justify-center rounded-lg text-xs font-black bg-blue-600 text-white shadow-lg">{page}</span>
              <span className="text-[10px] font-bold opacity-40">/ {totalPages}</span>
            </div>
            <button disabled={page >= totalPages} onClick={() => setPage(p => p + 1)} className="p-2 rounded-lg hover:bg-blue-500/10 disabled:opacity-20 transition-all"><ChevronRight size={16} /></button>
            <button disabled={page >= totalPages} onClick={() => setPage(totalPages)} className="p-2 rounded-lg hover:bg-blue-500/10 disabled:opacity-20 transition-all"><ChevronsRight size={16} /></button>
          </div>
        </div>
      </div>
    </div>
  );
}