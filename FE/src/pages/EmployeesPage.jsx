import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { 
  UserPlus, Search, Edit3, Trash2, X, Save, Loader2, 
  Mail, Eye, Phone, Calendar, Globe, MapPin, Award,
  CheckCircle2, AlertCircle, Info, ChevronRight, ChevronLeft,
  ChevronsLeft, ChevronsRight, TrendingUp, CreditCard, 
  CalendarDays, Wallet, ArrowUpRight, ArrowDownRight, History 
} from 'lucide-react';
import { useOutletContext } from 'react-router-dom';

// Định nghĩa API URL
const API_BASE = `${import.meta.env.VITE_API_URL}/api/v1/employees/`;
const API_DEPT = `${import.meta.env.VITE_API_URL}/api/v1/departments/`;
const API_POS = `${import.meta.env.VITE_API_URL}/api/v1/positions/`;

export default function EmployeesPage() {
  const { isDarkMode, language } = useOutletContext();
  
  // --- STATES DỮ LIỆU ---
  const [employees, setEmployees] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [positions, setPositions] = useState([]);
  
  // --- TRẠNG THÁI UI ---
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('');

  // --- PHÂN TRANG ---
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [totalPages, setTotalPages] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);

  // --- MODALS & SIDEBAR ---
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isDetailOpen, setIsDetailOpen] = useState(false);
  const [selectedEmp, setSelectedEmp] = useState(null);
  const [detailData, setDetailData] = useState(null);
  const [toast, setToast] = useState({ show: false, message: '', type: 'success' });
  const [confirmModal, setConfirmModal] = useState({ show: false, id: null });

  const [formData, setFormData] = useState({
    FullName: '', Email: '', PhoneNumber: '', 
    DepartmentID: '', PositionID: '', Status: 'Đang làm việc',
    Gender: 'Nam', DateOfBirth: '', HireDate: ''
  });

  // --- NGÔN NGỮ ---
  const t = {
    vi: {
      title: "Quản Lý Nhân Sự",
      addBtn: "Thêm nhân viên",
      table: { name: "Nhân viên", dept: "Phòng / Chức vụ", status: "Trạng thái", action: "Thao tác" },
      filters: { allStatus: "Tất cả trạng thái", search: "Tìm tên nhân viên...", page: "Trang", total: "Tổng" },
      form: { add: "Thêm nhân viên mới", edit: "Cập nhật thông tin", save: "Lưu dữ liệu", loading: "Đang xử lý..." },
      confirmDelete: "Bạn có chắc chắn muốn xóa nhân viên này? Dữ liệu sẽ được đồng bộ xóa trên toàn hệ thống.",
      msg: { success: "Cập nhật thành công!", error: "Lỗi kết nối máy chủ!", deleted: "Đã xóa nhân viên khỏi hệ thống." }
    },
    en: {
      title: "Employee Management",
      addBtn: "Add Employee",
      table: { name: "Employee", dept: "Dept / Position", status: "Status", action: "Actions" },
      filters: { allStatus: "All Status", search: "Search name...", page: "Page", total: "Total" },
      form: { add: "Add New Employee", edit: "Edit Employee", save: "Save Changes", loading: "Processing..." },
      confirmDelete: "Are you sure you want to delete this employee? This will sync across databases.",
      msg: { success: "Updated successfully!", error: "Server connection failed!", deleted: "Employee removed." }
    }
  }[language || 'vi'];
const [filters, setFilters] = useState({
  name: '',
  dept_id: '',
  pos_id: '',
  status: '',
  gender: '',
  start_date: '',
  end_date: ''
});
  const showToast = (message, type = 'success') => {
    setToast({ show: true, message, type });
    setTimeout(() => setToast(prev => ({ ...prev, show: false })), 3000);
  };

  // --- 1. LẤY DANH MỤC PHÒNG BAN & CHỨC VỤ ---
  const fetchMetadata = async () => {
    try {
      const [deptRes, posRes] = await Promise.all([
        axios.get(API_DEPT),
        axios.get(API_POS)
      ]);
      setDepartments(deptRes.data.data || []);
      setPositions(posRes.data.data || []);
    } catch (err) {
      console.error("Lỗi lấy metadata:", err);
    }
  };

  // --- 2. LẤY DANH SÁCH NHÂN VIÊN ---
  const fetchEmployees = useCallback(async () => {
  setLoading(true);
  try {
    const res = await axios.get(API_BASE, {
      params: { 
        ...filters, 
        page: currentPage,
        limit: pageSize // Đảm bảo API nhận tham số limit
      }
    });
    const { data, totalPages, total_records } = res.data; 
    setEmployees(data || []);
    setTotalPages(totalPages || 1);
    setTotalRecords(total_records || 0);
  } catch (err) {
    showToast(t.msg.error, 'error');
  } finally { setLoading(false); }
}, [filters, currentPage, pageSize, t.msg.error]); // <--- Thêm pageSize vào đây
  useEffect(() => {
    fetchMetadata();
  }, []);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      fetchEmployees();
    }, 400);
    return () => clearTimeout(delayDebounceFn);
  }, [searchTerm, filterStatus, currentPage, pageSize, fetchEmployees]);

  // --- 3. XỬ LÝ SỰ KIỆN ---
  const handleOpenForm = (emp = null) => {
    if (emp) {
      setSelectedEmp(emp);
      setFormData({ 
        ...emp,
        // Cắt chuỗi ISO từ Database (YYYY-MM-DDTHH:mm...) thành YYYY-MM-DD để input date hiển thị được
        DateOfBirth: emp.DateOfBirth ? emp.DateOfBirth.split('T')[0] : '',
        HireDate: emp.HireDate ? emp.HireDate.split('T')[0] : ''
      });
    } else {
      setSelectedEmp(null);
      setFormData({
        FullName: '', Email: '', PhoneNumber: '', 
        DepartmentID: departments[0]?.DepartmentID || '', 
        PositionID: positions[0]?.PositionID || '', 
        Status: 'Đang làm việc',
        Gender: 'Nam', 
        DateOfBirth: '', 
        HireDate: new Date().toISOString().split('T')[0]
      });
    }
    setIsSidebarOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setActionLoading(true);
    try {
      if (selectedEmp) {
        await axios.put(`${API_BASE}${selectedEmp.EmployeeID}`, formData);
      } else {
        await axios.post(API_BASE, formData);
      }
      setIsSidebarOpen(false);
      showToast(t.msg.success, 'success');
      fetchEmployees();
    } catch (err){
      showToast(err.response?.data?.message || t.msg.error, 'error');
    } finally { setActionLoading(false); }
  };

  const handleConfirmDelete = async () => {
    try {
      await axios.delete(`${API_BASE}${confirmModal.id}`);
      setConfirmModal({ show: false, id: null });
      showToast(t.msg.deleted, 'success');
      fetchEmployees();
    } catch (err) {
      showToast(t.msg.error, 'error');
    }
  };

  const handleViewDetail = async (id) => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE}${id}`);
      setDetailData(res.data.data);
      setIsDetailOpen(true);
    } catch (err) {
      showToast(t.msg.error, 'error');
    } finally { setLoading(false); }
  };

  return (
    <div className={`relative w-full h-full p-4 flex flex-col gap-4 transition-all duration-300 ${isDarkMode ? 'text-slate-300 bg-slate-950' : 'text-slate-800 bg-slate-50'}`}>
      
      {/* TOAST */}
      {toast.show && (
        <div className={`fixed top-6 left-1/2 -translate-x-1/2 z-[100] flex items-center gap-3 px-6 py-3 rounded-2xl shadow-2xl animate-in fade-in slide-in-from-top-5 duration-300 ${toast.type === 'success' ? 'bg-emerald-500 text-white' : 'bg-red-500 text-white'}`}>
          {toast.type === 'success' ? <CheckCircle2 size={18} /> : <AlertCircle size={18} />}
          <span className="text-sm font-bold">{toast.message}</span>
        </div>
      )}

      {/* CONFIRM DELETE MODAL */}
      {confirmModal.show && (
        <div className="fixed inset-0 z-[90] flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-sm animate-in fade-in">
          <div className={`w-full max-w-sm rounded-3xl overflow-hidden shadow-2xl animate-in zoom-in-95 ${isDarkMode ? 'bg-slate-900 border border-slate-800' : 'bg-white'}`}>
            <div className="p-8 text-center">
              <div className="mx-auto w-16 h-16 bg-red-500/10 text-red-500 rounded-full flex items-center justify-center mb-4">
                <Trash2 size={28} />
              </div>
              <h3 className="text-lg font-black mb-2 uppercase italic tracking-tight">Xác nhận xóa?</h3>
              <p className="text-sm opacity-60 leading-relaxed">{t.confirmDelete}</p>
            </div>
            <div className="flex border-t border-slate-800/10">
              <button onClick={() => setConfirmModal({ show: false, id: null })} className="flex-1 py-4 text-xs font-bold uppercase hover:bg-slate-500/5 transition-colors">Hủy</button>
              <button onClick={handleConfirmDelete} className="flex-1 py-4 text-xs font-bold uppercase bg-red-600 text-white hover:bg-red-700 transition-colors">Xóa</button>
            </div>
          </div>
        </div>
      )}

      {/* HEADER */}
      {/* SEARCH & FILTER BAR */}
       <div className="flex items-center gap-3">
          <h1 className="text-xl font-black uppercase border-l-4 border-blue-600 pl-3 leading-none italic">{t.title}</h1>
          
        </div>
<div className={`p-4 border mb-4 space-y-4 ${isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
 
  <div className="flex flex-wrap items-center gap-3">
    {/* Tìm tên */}
    <div className={`relative flex-1 min-w-[250px] flex items-center rounded-xs border transition-colors ${isDarkMode ? 'bg-slate-900 border-slate-800 focus-within:border-blue-500' : 'bg-white border-slate-200 focus-within:border-blue-400'}`}>
      <Search size={16} className="absolute left-3 opacity-40" />
      <input 
        type="text" placeholder="Tìm tên nhân viên..."
        className="bg-transparent border-none focus:ring-0 text-sm pl-10 pr-3 py-2 w-full"
        value={filters.name} 
        onChange={(e) => setFilters({...filters, name: e.target.value, page: 1})}
      />
    </div>

    {/* Lọc Phòng ban */}
    <select 
      value={filters.dept_id} 
      onChange={(e) => setFilters({...filters, dept_id: e.target.value, page: 1})}
      className={`text-sm font-medium rounded-xs border px-3 py-2 outline-none cursor-pointer ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'}`}
    >
      <option value="">Phòng ban</option>
      {departments.map(d => <option key={d.DepartmentID} value={d.DepartmentID}>{d.DepartmentName}</option>)}
    </select>

    {/* Lọc Trạng thái */}
    <select 
      value={filters.status} 
      onChange={(e) => setFilters({...filters, status: e.target.value, page: 1})}
      className={`text-sm font-medium rounded-xs border px-3 py-2 outline-none cursor-pointer ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'}`}
    >
      <option value="">Trạng thái</option>
      <option value="Đang làm việc">🟢 Đang làm việc</option>
      <option value="Nghỉ phép">🟡 Nghỉ phép</option>
      <option value="Thử việc">🔵 Thử việc</option>
    </select>

    {/* Nút Reset */}
    <button 
      onClick={() => setFilters({ name: '', dept_id: '', pos_id: '', status: '', gender: '', start_date: '', end_date: '' })}
      className="p-2.5 text-slate-500 hover:text-red-500 transition-colors"
      title="Xóa bộ lọc"
    >
      <X size={20} />
    </button>
  </div>

  {/* FILTER HÀNG 2: Nâng cao */}
  <div className="flex flex-wrap items-center gap-3 pt-3 border-t border-slate-800/10">
    {/* Chức vụ */}
    <select 
      value={filters.pos_id} 
      onChange={(e) => setFilters({...filters, pos_id: e.target.value, page: 1})}
      className={`text-[12px] font-bold rounded-xl border px-3 py-2 outline-none ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'}`}
    >
      <option value="">Chức vụ</option>
      {positions.map(p => <option key={p.PositionID} value={p.PositionID}>{p.PositionName}</option>)}
    </select>

    {/* Giới tính */}
    <select 
      value={filters.gender} 
      onChange={(e) => setFilters({...filters, gender: e.target.value, page: 1})}
      className={`text-[12px] font-bold rounded-xl border px-3 py-2 outline-none ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'}`}
    >
      <option value="">Giới tính</option>
      <option value="Nam">Nam</option>
      <option value="Nữ">Nữ</option>
    </select>

    {/* Khoảng ngày vào làm */}
    <div className="flex items-center gap-2">
      <span className="text-[10px] font-black uppercase opacity-40">Vào làm:</span>
      <input 
        type="date" 
        value={filters.start_date}
        onChange={(e) => setFilters({...filters, start_date: e.target.value, page: 1})}
        className={`text-[12px] rounded-lg border px-2 py-1.5 ${isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-slate-50 border-slate-200'}`} 
      />
      <span className="opacity-30">→</span>
      <input 
        type="date" 
        value={filters.end_date}
        onChange={(e) => setFilters({...filters, end_date: e.target.value, page: 1})}
        className={`text-[12px] rounded-lg border px-2 py-1.5 ${isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-slate-50 border-slate-200'}`} 
      />
    </div>
    <button onClick={() => handleOpenForm()} className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-xl text-xs font-bold transition-all shadow-lg shadow-blue-600/20 active:scale-95">
            <UserPlus size={14} /> {t.addBtn}
          </button>
  </div>
</div>

      {/* BẢNG DỮ LIỆU */}
      <div className={`flex-1 rounded-xs  border  flex flex-col ${isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
        <div className="flex-1  rounded-xs  overflow-y-auto custom-scrollbar">
          <table className="w-full  text-left border-collapse">
            <thead className={`sticky top-0 z-10 text-[10px] uppercase font-bold tracking-wider ${isDarkMode ? 'bg-slate-800 text-slate-400' : 'bg-slate-50 text-slate-500'}`}>
              <tr>
                <th className="px-6 py-4">{t.table.name}</th>
                <th className="px-6 py-4">{t.table.dept}</th>
                <th className="px-6 py-4">{t.table.status}</th>
                <th className="px-6 py-4 text-right">{t.table.action}</th>
              </tr>
            </thead>
            <tbody className={`divide-y ${isDarkMode ? 'divide-slate-800' : 'divide-slate-100'} text-xs`}>
              {loading ? (
                <tr><td colSpan="4" className="py-24 text-center"><Loader2 className="animate-spin inline text-blue-500" size={32} /></td></tr>
              ) : employees.length === 0 ? (
                <tr><td colSpan="4" className="py-24 text-center opacity-40 font-bold uppercase tracking-widest text-[10px]">Không tìm thấy nhân viên</td></tr>
              ) : (
                employees.map((emp) => (
                  <tr key={emp.EmployeeID} className="hover:bg-blue-600/5 transition-all group">
                    <td className="px-6 py-2">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl flex items-center justify-center font-black text-white bg-gradient-to-br from-blue-500 to-indigo-600 shadow-inner">
                          {emp.FullName?.charAt(0).toUpperCase()}
                        </div>
                        <div>
                          <p className="font-bold text-sm">{emp.FullName}</p>
                          <p className="text-[10px] opacity-50 flex items-center gap-1"><Mail size={10}/> {emp.Email}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-2">
                      <div className="flex flex-col">
                        <span className="font-semibold text-blue-500">{emp.DepartmentName}</span>
                        <span className="text-[10px] opacity-50 font-medium">{emp.PositionName}</span>
                      </div>
                    </td>
                    <td className="px-6 py-2">
                      <span className={`px-2.5 py-1 rounded-lg text-[10px] font-bold ${
                        emp.Status === 'Đang làm việc' ? 'bg-green-500/10 text-green-500' : 
                        emp.Status === 'Thử việc' ? 'bg-blue-500/10 text-blue-500' : 'bg-amber-500/10 text-amber-500'
                      }`}>
                        • {emp.Status}
                      </span>
                    </td>
                    <td className="px-6 py-2 text-right">
                      <div className="flex justify-end gap-1 opacity-0 group-hover:opacity-100 transition-all">
                        <button onClick={() => handleViewDetail(emp.EmployeeID)} className="p-2 hover:bg-emerald-500/10 text-emerald-500 rounded-lg transition-colors"><Eye size={15}/></button>
                        <button onClick={() => handleOpenForm(emp)} className="p-2 hover:bg-blue-500/10 text-blue-500 rounded-lg transition-colors"><Edit3 size={15}/></button>
                        <button onClick={() => setConfirmModal({ show: true, id: emp.EmployeeID })} className="p-2 hover:bg-red-500/10 text-red-500 rounded-lg transition-colors"><Trash2 size={15}/></button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* PHÂN TRANG */}
        <div className={`px-6 py-3 border-t flex items-center justify-between gap-4 ${isDarkMode ? 'border-slate-800 bg-slate-900/60' : 'border-slate-100 bg-slate-50/50'}`}>
          <div className="flex items-center gap-4">
            <span className="text-[10px] font-bold uppercase opacity-50">
              {t.filters.total}: <span className={isDarkMode ? 'text-white' : 'text-slate-900'}>{totalRecords}</span>
            </span>
          </div>

          <div className="flex items-center gap-1">
            <button disabled={currentPage === 1} onClick={() => setCurrentPage(1)} className="p-2 rounded-lg hover:bg-blue-500/10 disabled:opacity-20 transition-all"><ChevronsLeft size={16} /></button>
            <button disabled={currentPage === 1} onClick={() => setCurrentPage(prev => prev - 1)} className="p-2 rounded-lg hover:bg-blue-500/10 disabled:opacity-20 transition-all"><ChevronLeft size={16} /></button>
            <div className="flex items-center px-4 gap-2">
              <span className="w-8 h-8 flex items-center justify-center rounded-lg text-xs font-black bg-blue-600 text-white shadow-lg">{currentPage}</span>
              <span className="text-[10px] font-bold opacity-40">/ {totalPages}</span>
            </div>
            <button disabled={currentPage === totalPages} onClick={() => setCurrentPage(prev => prev + 1)} className="p-2 rounded-lg hover:bg-blue-500/10 disabled:opacity-20 transition-all"><ChevronRight size={16} /></button>
            <button disabled={currentPage === totalPages} onClick={() => setCurrentPage(totalPages)} className="p-2 rounded-lg hover:bg-blue-500/10 disabled:opacity-20 transition-all"><ChevronsRight size={16} /></button>
          </div>
        </div>
      </div>

      {/* FORM SIDEBAR (ADD/EDIT) */}
      {isSidebarOpen && (
        <div className="fixed inset-0 z-[70] flex justify-end bg-slate-950/40 backdrop-blur-[2px] animate-in fade-in duration-300">
          <div className={`w-full max-w-lg h-full shadow-2xl flex flex-col animate-in slide-in-from-right duration-500 ${isDarkMode ? 'bg-slate-900 border-l border-slate-800' : 'bg-white'}`}>
            <div className="p-6 border-b flex justify-between items-center border-slate-800/10">
              <h2 className="text-lg font-black uppercase italic tracking-tighter">{selectedEmp ? t.form.edit : t.form.add}</h2>
              <button onClick={() => setIsSidebarOpen(false)} className="p-2 hover:bg-red-500/10 text-red-500 rounded-full transition-colors"><X size={20}/></button>
            </div>

            <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto p-6 space-y-5 custom-scrollbar">
              <div className="space-y-1.5">
                <label className="text-[10px] font-bold uppercase opacity-50 ml-1">Họ và tên</label>
                <input required value={formData.FullName} onChange={e => setFormData({...formData, FullName: e.target.value})} className={`w-full p-3.5 rounded-xl border text-sm outline-none focus:ring-2 focus:ring-blue-500/20 transition-all ${isDarkMode ? 'bg-slate-800/50 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'}`} placeholder="Nguyễn Văn A" />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-[10px] font-bold uppercase opacity-50 ml-1">Email</label>
                  <input type="email" required value={formData.Email} onChange={e => setFormData({...formData, Email: e.target.value})} className={`w-full p-3.5 rounded-xl border text-sm outline-none ${isDarkMode ? 'bg-slate-800/50 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'}`} />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[10px] font-bold uppercase opacity-50 ml-1">Số điện thoại</label>
                  <input value={formData.PhoneNumber} onChange={e => setFormData({...formData, PhoneNumber: e.target.value})} className={`w-full p-3.5 rounded-xl border text-sm outline-none ${isDarkMode ? 'bg-slate-800/50 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'}`} />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-[10px] font-bold uppercase opacity-50 ml-1">Phòng ban</label>
                  <select required value={formData.DepartmentID} onChange={e => setFormData({...formData, DepartmentID: e.target.value})} className={`w-full p-3.5 rounded-xl border text-sm outline-none cursor-pointer ${isDarkMode ? 'bg-slate-800/50 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'}`}>
                    <option value="">Chọn phòng ban</option>
                    {departments.map(dept => (
                      <option key={dept.DepartmentID} value={dept.DepartmentID}>{dept.DepartmentName}</option>
                    ))}
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[10px] font-bold uppercase opacity-50 ml-1">Chức vụ</label>
                  <select required value={formData.PositionID} onChange={e => setFormData({...formData, PositionID: e.target.value})} className={`w-full p-3.5 rounded-xl border text-sm outline-none cursor-pointer ${isDarkMode ? 'bg-slate-800/50 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'}`}>
                    <option value="">Chọn chức vụ</option>
                    {positions.map(pos => (
                      <option key={pos.PositionID} value={pos.PositionID}>{pos.PositionName}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-[10px] font-bold uppercase opacity-50 ml-1">Ngày sinh</label>
                  <input type="date" value={formData.DateOfBirth} onChange={e => setFormData({...formData, DateOfBirth: e.target.value})} className={`w-full p-3.5 rounded-xl border text-sm outline-none ${isDarkMode ? 'bg-slate-800/50 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'}`} />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[10px] font-bold uppercase opacity-50 ml-1">Giới tính</label>
                  <select value={formData.Gender} onChange={e => setFormData({...formData, Gender: e.target.value})} className={`w-full p-3.5 rounded-xl border text-sm outline-none cursor-pointer ${isDarkMode ? 'bg-slate-800/50 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'}`}>
                    <option value="Nam">Nam</option>
                    <option value="Nữ">Nữ</option>
                    <option value="Khác">Khác</option>
                  </select>
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="text-[10px] font-bold uppercase opacity-50 ml-1">Trạng thái công việc</label>
                <select value={formData.Status} onChange={e => setFormData({...formData, Status: e.target.value})} className={`w-full p-3.5 rounded-xl border text-sm outline-none cursor-pointer ${isDarkMode ? 'bg-slate-800/50 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'}`}>
                  <option value="Đang làm việc">🟢 Đang làm việc</option>
                  <option value="Nghỉ phép">🟡 Nghỉ phép</option>
                  <option value="Thử việc">🔵 Thử việc</option>
                </select>
              </div>

              <div className="pt-6">
                <button 
                  type="submit" disabled={actionLoading}
                  className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-bold py-4 rounded-2xl shadow-xl shadow-blue-600/20 flex items-center justify-center gap-2 transition-all active:scale-[0.98]"
                >
                  {actionLoading ? <Loader2 className="animate-spin" size={20} /> : <Save size={18} />} 
                  {actionLoading ? t.form.loading : t.form.save}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* DETAIL MODAL */}
      {isDetailOpen && detailData && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-md animate-in fade-in duration-200">
          <div className={`w-full max-w-4xl max-h-[92vh] overflow-hidden rounded-[2rem] shadow-2xl flex flex-col animate-in zoom-in-95 duration-200 ${isDarkMode ? 'bg-slate-900 border border-slate-800' : 'bg-white'}`}>
            <div className="p-6 border-b border-slate-800/10 flex justify-between items-center bg-gradient-to-r from-blue-600/5 to-transparent">
              <div className="flex items-center gap-3 text-blue-500">
                <div className="p-2 bg-blue-500/10 rounded-lg"><Info size={20}/></div>
                <h2 className="font-black uppercase tracking-widest text-sm italic">Hồ sơ nhân sự chi tiết</h2>
              </div>
              <button onClick={() => setIsDetailOpen(false)} className="p-2 hover:bg-red-500/10 text-red-500 rounded-full transition-colors"><X size={24}/></button>
            </div>
            
            <div className="flex-1 overflow-y-auto p-8 space-y-8 custom-scrollbar">
              <div className="flex flex-col md:flex-row items-center md:items-start gap-8 border-b border-slate-800/10 pb-8">
                <div className="relative">
                  <div className="w-32 h-32 rounded-[2.5rem] bg-gradient-to-br from-blue-500 to-indigo-700 flex items-center justify-center text-5xl font-black text-white shadow-2xl shadow-blue-500/20">
                    {detailData.FullName?.charAt(0)}
                  </div>
                  <div className="absolute -bottom-2 -right-2 bg-emerald-500 text-white p-2 rounded-2xl border-4 border-slate-900">
                    <CheckCircle2 size={16} />
                  </div>
                </div>
                
                <div className="flex-1 text-center md:text-left">
                  <h3 className="text-3xl font-black italic tracking-tighter mb-1">{detailData.FullName}</h3>
                  <div className="flex flex-wrap justify-center md:justify-start gap-3 items-center">
                    <span className="px-3 py-1 bg-blue-500/10 text-blue-500 rounded-full text-[10px] font-black uppercase tracking-widest">{detailData.PositionName}</span>
                    <span className="text-xs opacity-40 font-bold uppercase tracking-widest">{detailData.DepartmentName}</span>
                    <span className="w-1.5 h-1.5 rounded-full bg-slate-500 opacity-30"></span>
                    <span className="text-[10px] font-bold opacity-50 uppercase tracking-tighter">ID: EMP-{detailData.EmployeeID}</span>
                  </div>
                  
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                    <div className="p-3 rounded-2xl bg-slate-500/5 border border-slate-500/10">
                      <p className="text-[10px] font-bold opacity-40 uppercase mb-1">Giới tính</p>
                      <p className="text-sm font-black">{detailData.Gender}</p>
                    </div>
                    <div className="p-3 rounded-2xl bg-slate-500/5 border border-slate-500/10">
                      <p className="text-[10px] font-bold opacity-40 uppercase mb-1">Trạng thái</p>
                      <p className="text-sm font-black text-emerald-500">{detailData.Status}</p>
                    </div>
                    <div className="p-3 rounded-2xl bg-slate-500/5 border border-slate-500/10">
                      <p className="text-[10px] font-bold opacity-40 uppercase mb-1">Ngày gia nhập</p>
                      <p className="text-sm font-black">{new Date(detailData.HireDate).toLocaleDateString('vi-VN')}</p>
                    </div>
                    <div className="p-3 rounded-2xl bg-slate-500/5 border border-slate-500/10">
                      <p className="text-[10px] font-bold opacity-40 uppercase mb-1">Số điện thoại</p>
                      <p className="text-sm font-black">{detailData.PhoneNumber || '---'}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-black uppercase italic tracking-widest flex items-center gap-2">
                    <History size={18} className="text-blue-500"/> Diễn biến thu nhập (6 tháng gần nhất)
                  </h4>
                  
                </div>

                {detailData.salary_history && detailData.salary_history.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-3">
                      {detailData.salary_history.slice(0, 6).map((item, idx) => (
                        <div key={idx} className={`group flex items-center justify-between p-4 rounded-2xl border transition-all ${isDarkMode ? 'bg-slate-800/30 border-slate-800 hover:border-blue-500/50' : 'bg-slate-50 border-slate-200 hover:border-blue-300'}`}>
                          <div className="flex items-center gap-4">
                            <div className="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center text-blue-500 font-black text-xs">
                              T{new Date(item.SalaryMonth).getMonth() + 1}
                            </div>
                            <div>
                              <p className="text-xs font-black uppercase italic">Tháng {new Date(item.SalaryMonth).toLocaleDateString('vi-VN', {month: '2-digit', year: 'numeric'})}</p>
                              <p className="text-[10px] opacity-50 font-bold">Ngày nhận: {new Date(item.PaymentDate).toLocaleDateString('vi-VN')}</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="text-sm font-black text-blue-500">{new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(item.NetSalary)}</p>
                            <div className="flex items-center justify-end gap-1 text-[9px] font-bold text-emerald-500 italic">
                              <TrendingUp size={10}/> Đã thanh toán
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>

                    <div className="flex flex-col gap-4">
                      <div className={`flex-1 p-6 rounded-3xl border-2 border-dashed flex flex-col justify-center items-center text-center ${isDarkMode ? 'border-slate-800 bg-slate-900' : 'border-slate-100 bg-slate-50/50'}`}>
                        <Wallet size={32} className="text-blue-500 mb-3 opacity-50" />
                        <p className="text-[10px] font-black uppercase opacity-40 mb-1">Tổng thu nhập năm 2026</p>
                        <h5 className="text-2xl font-black italic tracking-tighter text-blue-500">
                          {new Intl.NumberFormat('vi-VN').format(detailData.salary_history.reduce((sum, item) => sum + item.NetSalary, 0))} <span className="text-xs italic">VND</span>
                        </h5>
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                         <div className="p-4 rounded-2xl bg-indigo-500/5 border border-indigo-500/10 text-center">
                            <p className="text-[9px] font-black uppercase opacity-50 mb-1">Trung bình tháng</p>
                            <p className="text-sm font-black italic">~ 15.5M</p>
                         </div>
                         <div className="p-4 rounded-2xl bg-emerald-500/5 border border-emerald-500/10 text-center">
                            <p className="text-[9px] font-black uppercase opacity-50 mb-1">Công chuẩn</p>
                            <p className="text-sm font-black italic">26 Ngày</p>
                         </div>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="py-12 flex flex-col items-center opacity-30">
                     <CreditCard size={40} className="mb-2"/>
                     <p className="text-xs font-bold uppercase italic">Chưa có dữ liệu lương phát sinh</p>
                  </div>
                )}
              </div>
            </div>
            
            <div className="p-6 border-t border-slate-800/10 bg-slate-500/5 flex justify-between gap-4">
              <button className="flex-1 py-3 rounded-xl bg-slate-500/10 text-xs font-black uppercase italic hover:bg-slate-500/20 transition-all">Xuất File PDF</button>
              <button onClick={() => { setIsDetailOpen(false); handleOpenForm(detailData); }} className="flex-1 py-3 rounded-xl bg-blue-600 text-white text-xs font-black uppercase italic hover:bg-blue-700 shadow-lg shadow-blue-600/20 transition-all">Chỉnh sửa hồ sơ</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}