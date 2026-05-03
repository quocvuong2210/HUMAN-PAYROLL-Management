import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { 
  Briefcase, Landmark, Search, Plus, Edit3, Trash2, 
  Loader2, X, Users, RefreshCw, CheckCircle2, AlertTriangle, Coins
} from 'lucide-react';
import { useOutletContext } from 'react-router-dom';

const API_DEPT = `${import.meta.env.VITE_API_URL}/api/v1/departments`;
const API_POS = `${import.meta.env.VITE_API_URL}/api/v1/positions`;

export default function DepartmentsPage() {
  const { isDarkMode, language } = useOutletContext();
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('dept'); 
  const [data, setData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  
  // Modal State
  const [showModal, setShowModal] = useState(false);
  const [modalMode, setModalMode] = useState('create'); 
  const [selectedItem, setSelectedItem] = useState(null);
  const [formData, setFormData] = useState({ name: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Đa ngôn ngữ mở rộng
  const t = {
    vi: {
      dept: "Phòng Ban", pos: "Chức Vụ", add: "Thêm mới",
      search: "Tìm tên hoặc mã...", noData: "Không tìm thấy dữ liệu",
      actions: "Thao tác", confirmDelete: "Xóa mục này?",
      stats: "Nhân sự", salary: "Quỹ lương", sync: "Đồng bộ Master-Slave",
      id: "Mã", name: "Tên gọi", finish: "Hoàn tất", update: "Cập nhật"
    },
    
    en: {
      dept: "Departments", pos: "Positions", add: "Add New",
      search: "Search name/ID...", noData: "No data found",
      actions: "Actions", confirmDelete: "Confirm delete?",
      stats: "Staff", salary: "Payroll", sync: "Sync Master-Slave",
      id: "ID", name: "Name", finish: "Finish", update: "Update"
    }
  }[language || 'vi'];

  // 1. FETCH DATA
  const fetchData = useCallback(async () => {
    setLoading(true);
    const endpoint = activeTab === 'dept' ? `${API_DEPT}/` : `${API_POS}/`;
    
    try {
      const response = await axios.get(endpoint, {
        params: { search: searchTerm }
      });
      setData(response.data.data || []);
    } catch (err) {
      console.error("Fetch error:", err);
      setData([]);
    } finally {
      setLoading(false);
    }
  }, [activeTab, searchTerm]);

  useEffect(() => { fetchData(); }, [fetchData]);

  // 2. CUD OPERATIONS
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name.trim()) return;
    setIsSubmitting(true);
    
    const endpoint = activeTab === 'dept' ? API_DEPT : API_POS;
    const nameKey = activeTab === 'dept' ? 'DepartmentName' : 'PositionName';
    const idKey = activeTab === 'dept' ? 'DepartmentID' : 'PositionID';

    try {
      if (modalMode === 'create') {
        await axios.post(`${endpoint}/`, { [nameKey]: formData.name });
      } else {
        await axios.put(`${endpoint}/${selectedItem[idKey]}`, { [nameKey]: formData.name });
      }
      setShowModal(false);
      setFormData({ name: '' });
      fetchData();
    } catch (err) {
      alert("Lỗi: " + (err.response?.data?.error || "Thao tác thất bại"));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (item) => {
    const idKey = activeTab === 'dept' ? 'DepartmentID' : 'PositionID';
    const name = activeTab === 'dept' ? item.DepartmentName : item.PositionName;
    
    if (window.confirm(`${t.confirmDelete}\n[${name}]`)) {
      try {
        const endpoint = activeTab === 'dept' ? API_DEPT : API_POS;
        await axios.delete(`${endpoint}/${item[idKey]}`);
        fetchData();
      } catch (err) {
        alert("Không thể xóa: " + (err.response?.data?.error || "Mục này đang có dữ liệu liên kết"));
      }
    }
  };

  const handleSync = async () => {
    setLoading(true);
    try {
      const endpoint = activeTab === 'dept' ? API_DEPT : API_POS;
      await axios.post(`${endpoint}/sync`);
      fetchData();
    } catch (err) { 
        alert("Đồng bộ thất bại!");
    } finally { setLoading(false); }
  };

  // Helper định dạng tiền tệ
  const formatVND = (amount) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount || 0);
  };

  return (
    <div className={`w-full h-full p-4 flex flex-col gap-4 transition-all duration-300 ${isDarkMode ? 'text-slate-300 bg-slate-950' : 'text-slate-800 bg-slate-50'}`}>
      
      {/* 1. HEADER & SEARCH */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <h1 className="text-xl font-black uppercase border-l-4 border-blue-600 pl-3 leading-none italic">{t.dept}</h1>
          
        </div>
        <div className="flex items-center gap-2">
          <div className={`relative flex items-center rounded-xl border w-full md:w-72 ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
            <Search size={14} className="absolute left-3 opacity-40" />
            <input 
              type="text" placeholder={t.search}
              className="bg-transparent border-none focus:ring-0 text-xs pl-10 pr-3 py-3 w-full font-medium"
              value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <button 
            onClick={() => { setModalMode('create'); setFormData({name: ''}); setShowModal(true); }}
            className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-5 py-3 rounded-xl text-xs font-black uppercase tracking-widest transition-all shadow-lg shadow-blue-500/25 shrink-0"
          >
            <Plus size={16} strokeWidth={3} />
            <span className="hidden sm:inline">{t.add}</span>
          </button>
        </div>
      </div>

      {/* 2. TAB SELECTOR */}
     {/* 2. TAB SELECTOR */}
<div className="flex gap-6 border-b border-gray-200">
  {/* Nút 1: Phòng Ban (DEPT) */}
  <button 
    onClick={() => { setActiveTab('dept'); }} 
    className={`pb-2 flex items-center gap-2 border-b-2 transition-all duration-200 ${
      activeTab === 'dept' 
        ? 'border-blue-500 text-blue-500 font-semibold' 
        : 'border-transparent text-gray-500 hover:text-gray-700'
    }`}
  >
    <Landmark size={16} /> {t.dept}
  </button>

  {/* Nút 2: Chức Vụ (POS) */}
  <button 
    onClick={() => { setActiveTab('pos'); }} 
    className={`pb-2 flex items-center gap-2 border-b-2 transition-all duration-200 ${
      activeTab === 'pos' 
        ? 'border-blue-500 text-blue-500 font-semibold' 
        : 'border-transparent text-gray-500 hover:text-gray-700'
    }`}
  >
    <Briefcase size={16} /> {t.pos}
  </button>
</div>
      {/* 3. TABLE AREA */}
      <div className={`flex-1 border flex flex-col overflow-hidden ${isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
        <div className="flex-1 overflow-y-auto custom-scrollbar">
          <table className={`divide-y ${isDarkMode ? 'divide-slate-800' : 'divide-slate-100'} text-xs w-full`}>
            <thead className={`sticky top-0 z-10 text-[10px] uppercase font-black tracking-[0.15em] ${isDarkMode ? 'bg-slate-800/90 text-slate-400' : 'bg-slate-50/90 text-slate-500'} backdrop-blur-md`}>
              <tr>
                <th className="px-8 py-5 w-24">{t.id}</th>
                <th className="px-6 py-5">{t.name}</th>
                {activeTab === 'dept' && (
                  <>
                    <th className="px-6 py-5">{t.stats}</th>
                    <th className="px-6 py-5">{t.salary}</th>
                  </>
                )}
                <th className="px-8 py-5 text-right">{t.actions}</th>
              </tr>
            </thead>
            <tbody className={`divide-y ${isDarkMode ? 'divide-slate-800' : 'divide-slate-100'} text-xs`}>
              {loading ? (
                <tr><td colSpan={activeTab === 'dept' ? "6" : "4"} className="py-32 text-center"><Loader2 className="animate-spin inline text-blue-500" size={40} /></td></tr>
              ) : data.length > 0 ? (
                data.map((item) => {
                  const id = activeTab === 'dept' ? item.DepartmentID : item.PositionID;
                  const name = activeTab === 'dept' ? item.DepartmentName : item.PositionName;
                  
                  return (
                    <tr key={`${activeTab}-${id}`} className="hover:bg-blue-600/[0.03] transition-all group">
                      <td className="px-8 py-2 font-mono text-[10px] opacity-40 font-bold">#{id}</td>
                      <td className="px-6 py-2">
                        <div className="flex items-center gap-4">
                          <div className={`w-10 h-10 rounded-2xl flex items-center justify-center font-black text-xs shadow-sm ${isDarkMode ? 'bg-slate-800 text-blue-400' : 'bg-blue-100 text-blue-600'}`}>
                            {name?.charAt(0)}
                          </div>
                          <span className="font-black text-sm tracking-tight">{name}</span>
                        </div>
                      </td>
                      
                      {activeTab === 'dept' && (
                        <>
                          <td className="px-6 py-2">
                            <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full w-fit font-black text-[10px] ${item.TotalEmployees > 0 ? 'bg-green-500/10 text-green-500 ring-1 ring-green-500/20' : 'bg-slate-500/10 text-slate-400'}`}>
                              <Users size={12} strokeWidth={3} />
                              <span>{item.TotalEmployees || 0} {t.stats.toUpperCase()}</span>
                            </div>
                          </td>
                          <td className="px-6 py-2">
                            <div className={`flex items-center gap-2 font-mono font-bold text-[11px] ${isDarkMode ? 'text-blue-400' : 'text-blue-700'}`}>
                              <Coins size={12} className="opacity-50" />
                              {formatVND(item.TotalSalary)}
                            </div>
                          </td>
                        </>
                      )}

                      <td className="px-8 py-2 text-right">
                        <div className="flex items-center justify-end gap-1 opacity-0 group-hover:opacity-100 transition-all transform translate-x-2 group-hover:translate-x-0">
                          <button 
                            onClick={() => { setModalMode('edit'); setSelectedItem(item); setFormData({name}); setShowModal(true); }}
                            className={`p-2.5 rounded-xl transition-all ${isDarkMode ? 'hover:bg-blue-500/20 text-slate-400 hover:text-blue-400' : 'hover:bg-blue-50 text-slate-400 hover:text-blue-600'}`}
                          >
                            <Edit3 size={15} />
                          </button>
                          <button 
                            onClick={() => handleDelete(item)}
                            className={`p-2.5 rounded-xl transition-all ${isDarkMode ? 'hover:bg-red-500/20 text-slate-400 hover:text-red-400' : 'hover:bg-red-50 text-slate-400 hover:text-red-500'}`}
                          >
                            <Trash2 size={15} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  )
                })
              ) : (
                <tr>
                  <td colSpan={activeTab === 'dept' ? "6" : "4"} className="py-32 text-center">
                    <div className="flex flex-col items-center opacity-20">
                      <AlertTriangle size={48} className="mb-2" />
                      <p className="text-sm font-black uppercase tracking-widest">{t.noData}</p>
                    </div>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* 4. MODAL (CREATE / EDIT) */}
      {showModal && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 animate-in fade-in duration-200">
          <div className="absolute inset-0 bg-slate-950/80 backdrop-blur-md" onClick={() => setShowModal(false)} />
          <div className={`relative w-full max-w-md rounded-[2.5rem] shadow-2xl border p-8 animate-in zoom-in-95 duration-300 ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'}`}>
            
            <div className="flex justify-between items-start mb-8">
              <div>
                <h3 className="text-2xl font-black uppercase tracking-tighter leading-none mb-2">
                  {modalMode === 'create' ? t.add : t.update}
                </h3>
                <p className="text-[10px] font-bold text-blue-500 uppercase tracking-[0.2em]">
                  {activeTab === 'dept' ? t.dept : t.pos}
                </p>
              </div>
              <button onClick={() => setShowModal(false)} className={`p-2 rounded-full transition-colors ${isDarkMode ? 'hover:bg-slate-800' : 'hover:bg-slate-100'}`}><X size={24} /></button>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-8">
              <div className="space-y-3">
                <label className="text-[10px] font-black uppercase tracking-widest opacity-40 ml-1">{t.name}</label>
                <input 
                  autoFocus required type="text"
                  className={`w-full px-6 py-4 rounded-2xl border-2 outline-none transition-all font-black text-lg ${isDarkMode ? 'bg-slate-950 border-slate-800 focus:border-blue-600' : 'bg-slate-50 border-slate-100 focus:border-blue-500 focus:bg-white'}`}
                  placeholder="..."
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                />
              </div>

              <div className="flex gap-4">
                <button 
                  type="submit" disabled={isSubmitting}
                  className="flex-1 py-4 rounded-2xl font-black text-xs uppercase tracking-[0.2em] bg-blue-600 hover:bg-blue-700 text-white shadow-xl shadow-blue-500/30 transition-all flex items-center justify-center gap-3 disabled:opacity-50"
                >
                  {isSubmitting ? <Loader2 size={18} className="animate-spin" /> : <CheckCircle2 size={18} strokeWidth={3} />}
                  {t.finish}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}