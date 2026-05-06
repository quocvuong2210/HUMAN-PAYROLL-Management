import { useState, useEffect } from 'react';
import axios from 'axios';
import { useToast } from '../contexts/ToastContext';
import { useOutletContext } from 'react-router-dom';
import {
    Gift, Plus, Edit3, Trash2, X, Loader2,
    CheckCircle2, AlertCircle, RefreshCw, Calendar,
    DollarSign, Users, TrendingUp
} from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const DividendsPage = () => {
    const { isDarkMode, language } = useOutletContext() || { isDarkMode: false, language: 'vi' };
    const [dividends, setDividends] = useState([]);
    const [statistics, setStatistics] = useState(null);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [editingDividend, setEditingDividend] = useState(null);
    const [filterYear, setFilterYear] = useState(new Date().getFullYear());
    const [confirmModal, setConfirmModal] = useState({ show: false, id: null });
    const [isSubmitting, setIsSubmitting] = useState(false);

    const { showToast } = useToast();

    // Translations
    const t = {
        vi: {
            title: 'Quản Lý Thưởng',
            subtitle: 'Quản lý cổ tức và thưởng cho nhân viên',
            refresh: 'Làm mới',
            addNew: 'Tạo Thưởng Mới',
            totalDividends: 'Tổng Thưởng',
            totalAmount: 'Tổng Tiền',
            average: 'Trung Bình',
            year: 'Năm',
            allYears: 'Tất cả',
            loading: 'Đang tải...',
            noData: 'Không có dữ liệu',
            id: 'ID',
            employee: 'Nhân Viên',
            amount: 'Số Tiền',
            date: 'Ngày',
            createdAt: 'Tạo Lúc',
            actions: 'Hành Động',
            confirmDelete: 'Xác nhận xóa?',
            deleteMessage: 'Bạn có chắc chắn muốn xóa thưởng này? Dữ liệu sẽ bị xóa vĩnh viễn.',
            cancel: 'Hủy',
            delete: 'Xóa',
            createTitle: 'Tạo Thưởng Mới',
            updateTitle: 'Cập Nhật Thưởng',
            employeeId: 'ID Nhân Viên',
            amountVnd: 'Số Tiền (VND)',
            issueDate: 'Ngày Phát',
            save: 'Lưu',
            update: 'Cập Nhật',
            create: 'Tạo Mới'
        },
        en: {
            title: 'Dividend Management',
            subtitle: 'Manage employee dividends and bonuses',
            refresh: 'Refresh',
            addNew: 'Add Dividend',
            totalDividends: 'Total Dividends',
            totalAmount: 'Total Amount',
            average: 'Average',
            year: 'Year',
            allYears: 'All Years',
            loading: 'Loading...',
            noData: 'No data',
            id: 'ID',
            employee: 'Employee',
            amount: 'Amount',
            date: 'Date',
            createdAt: 'Created At',
            actions: 'Actions',
            confirmDelete: 'Confirm Delete?',
            deleteMessage: 'Are you sure you want to delete this dividend? This action cannot be undone.',
            cancel: 'Cancel',
            delete: 'Delete',
            createTitle: 'Create New Dividend',
            updateTitle: 'Update Dividend',
            employeeId: 'Employee ID',
            amountVnd: 'Amount (VND)',
            issueDate: 'Issue Date',
            save: 'Save',
            update: 'Update',
            create: 'Create'
        }
    }[language || 'vi'];

    const [formData, setFormData] = useState({
        employee_id: '',
        amount: '',
        date: new Date().toISOString().split('T')[0]
    });

    // Fetch dividends
    const fetchDividends = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_URL}/api/v1/dividends`, {
                headers: { Authorization: `Bearer ${token}` }
            });

            if (response.data.status === 'success') {
                setDividends(response.data.data);
            }
        } catch (error) {
            console.error('Error fetching dividends:', error);
            showToast('Lỗi tải danh sách thưởng', 'error');
        } finally {
            setLoading(false);
        }
    };

    // Fetch statistics
    const fetchStatistics = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_URL}/api/v1/dividends/statistics`, {
                headers: { Authorization: `Bearer ${token}` }
            });

            if (response.data.status === 'success') {
                setStatistics(response.data.data);
            }
        } catch (error) {
            console.error('Error fetching statistics:', error);
        }
    };

    useEffect(() => {
        fetchDividends();
        fetchStatistics();
    }, []);

    // Handle form submit
    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);

        try {
            const token = localStorage.getItem('token');

            if (editingDividend) {
                // Update
                await axios.put(
                    `${API_URL}/api/v1/dividends/${editingDividend.DividendID}`,
                    formData,
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                showToast('Cập nhật thưởng thành công', 'success');
            } else {
                // Create
                await axios.post(
                    `${API_URL}/api/v1/dividends`,
                    formData,
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                showToast('Tạo thưởng thành công', 'success');
            }

            setShowModal(false);
            resetForm();
            fetchDividends();
            fetchStatistics();
        } catch (error) {
            console.error('Error saving dividend:', error);
            showToast(error.response?.data?.message || 'Lỗi lưu thưởng', 'error');
        } finally {
            setIsSubmitting(false);
        }
    };

    // Handle delete
    const handleDelete = async (dividendId) => {
        setConfirmModal({ show: true, id: dividendId });
    };

    const handleConfirmDelete = async () => {
        try {
            const token = localStorage.getItem('token');
            await axios.delete(`${API_URL}/api/v1/dividends/${confirmModal.id}`, {
                headers: { Authorization: `Bearer ${token}` }
            });

            showToast('Xóa thưởng thành công', 'success');
            setConfirmModal({ show: false, id: null });
            fetchDividends();
            fetchStatistics();
        } catch (error) {
            console.error('Error deleting dividend:', error);
            showToast('Lỗi xóa thưởng', 'error');
            setConfirmModal({ show: false, id: null });
        }
    };

    // Handle edit
    const handleEdit = (dividend) => {
        setEditingDividend(dividend);
        setFormData({
            employee_id: dividend.EmployeeID,
            amount: dividend.DividendAmount,
            date: dividend.DividendDate
        });
        setShowModal(true);
    };

    // Reset form
    const resetForm = () => {
        setFormData({
            employee_id: '',
            amount: '',
            date: new Date().toISOString().split('T')[0]
        });
        setEditingDividend(null);
    };

    // Format currency
    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('vi-VN', {
            style: 'currency',
            currency: 'VND'
        }).format(amount);
    };

    // Filter dividends
    const filteredDividends = dividends.filter(d => {
        if (filterYear && new Date(d.DividendDate).getFullYear() !== parseInt(filterYear)) return false;
        return true;
    });

    return (
        <div className={`relative w-full h-full p-6 flex flex-col gap-6 transition-all duration-300 ${isDarkMode ? 'text-slate-300 bg-slate-950' : 'text-slate-800 bg-slate-50'}`}>

            {/* CONFIRM DELETE MODAL */}
            {confirmModal.show && (
                <div className="fixed inset-0 z-[90] flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-sm animate-in fade-in">
                    <div className={`w-full max-w-sm rounded-3xl overflow-hidden shadow-2xl animate-in zoom-in-95 ${isDarkMode ? 'bg-slate-900 border border-slate-800' : 'bg-white'}`}>
                        <div className="p-8 text-center">
                            <div className="mx-auto w-16 h-16 bg-red-500/10 text-red-500 rounded-full flex items-center justify-center mb-4">
                                <Trash2 size={28} />
                            </div>
                            <h3 className="text-lg font-black mb-2 uppercase italic tracking-tight">{t.confirmDelete}</h3>
                            <p className="text-sm opacity-60 leading-relaxed">
                                {t.deleteMessage}
                            </p>
                        </div>
                        <div className="flex border-t border-slate-800/10">
                            <button
                                onClick={() => setConfirmModal({ show: false, id: null })}
                                className="flex-1 py-4 text-xs font-bold uppercase hover:bg-slate-500/5 transition-colors"
                            >
                                {t.cancel}
                            </button>
                            <button
                                onClick={handleConfirmDelete}
                                className="flex-1 py-4 text-xs font-bold uppercase bg-red-600 text-white hover:bg-red-700 transition-colors"
                            >
                                {t.delete}
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Header */}
            <div className={`flex items-center justify-between border-b pb-4 ${isDarkMode ? 'border-slate-700' : 'border-gray-200'}`}>
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center">
                        <Gift size={20} className="text-white" />
                    </div>
                    <div>
                        <h1 className="text-2xl font-black tracking-tight">{t.title}</h1>
                        <p className={`text-xs font-medium ${isDarkMode ? 'text-slate-400' : 'text-gray-500'}`}>{t.subtitle}</p>
                    </div>
                </div>
                <div className="flex items-center gap-2">
                    <button
                        onClick={() => { fetchDividends(); fetchStatistics(); }}
                        disabled={loading}
                        className="text-xs px-3 py-1.5 bg-blue-600/10 text-blue-600 rounded-lg flex items-center gap-2 hover:bg-blue-600/20 disabled:opacity-50"
                    >
                        <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
                        {t.refresh}
                    </button>
                    <button
                        onClick={() => {
                            resetForm();
                            setShowModal(true);
                        }}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-1.5 rounded-lg font-semibold text-sm flex items-center gap-2 shadow-lg shadow-blue-600/20 transition-all"
                    >
                        <Plus size={16} strokeWidth={3} />
                        {t.addNew}
                    </button>
                </div>
            </div>

            {/* Statistics Cards */}
            {statistics && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className={`p-5 rounded-xl border shadow-sm ${isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200'}`}>
                        <div className="flex items-center gap-3 mb-2">
                            <div className="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center">
                                <Gift size={18} className="text-blue-500" />
                            </div>
                            <p className="text-xs font-black text-slate-500 uppercase tracking-wider">{t.totalDividends}</p>
                        </div>
                        <p className="text-3xl font-black text-blue-600">{statistics.TotalDividends}</p>
                    </div>
                    <div className={`p-5 rounded-xl border shadow-sm ${isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200'}`}>
                        <div className="flex items-center gap-3 mb-2">
                            <div className="w-10 h-10 rounded-xl bg-green-500/10 flex items-center justify-center">
                                <DollarSign size={18} className="text-green-500" />
                            </div>
                            <p className="text-xs font-black text-slate-500 uppercase tracking-wider">{t.totalAmount}</p>
                        </div>
                        <p className="text-3xl font-black text-green-600">
                            {formatCurrency(statistics.TotalAmount)}
                        </p>
                    </div>
                    <div className={`p-5 rounded-xl border shadow-sm ${isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200'}`}>
                        <div className="flex items-center gap-3 mb-2">
                            <div className="w-10 h-10 rounded-xl bg-purple-500/10 flex items-center justify-center">
                                <TrendingUp size={18} className="text-purple-500" />
                            </div>
                            <p className="text-xs font-black text-slate-500 uppercase tracking-wider">{t.average}</p>
                        </div>
                        <p className="text-3xl font-black text-purple-600">
                            {formatCurrency(statistics.AverageAmount)}
                        </p>
                    </div>
                </div>
            )}

            {/* Filters */}
            <div className={`p-4 rounded-xl border shadow-sm ${isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200'}`}>
                <div className="flex gap-4 items-center">
                    <div className="flex items-center gap-2">
                        <Calendar size={16} className="text-slate-400" />
                        <label className="text-xs font-black text-slate-500 uppercase tracking-wider">{t.year}</label>
                    </div>
                    <select
                        value={filterYear}
                        onChange={(e) => setFilterYear(e.target.value)}
                        className={`text-sm font-medium rounded-lg border px-3 py-2 outline-none cursor-pointer ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'}`}
                    >
                        <option value="">{t.allYears}</option>
                        {[2026, 2025, 2024, 2023].map(year => (
                            <option key={year} value={year}>{year}</option>
                        ))}
                    </select>
                </div>
            </div>

            {/* Table */}
            <div className={`flex-1 rounded-xl border shadow-sm flex flex-col overflow-hidden ${isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200'}`}>
                {loading ? (
                    <div className="flex-1 flex items-center justify-center">
                        <div className="text-center">
                            <Loader2 className="animate-spin inline text-blue-500 mb-4" size={40} />
                            <p className="text-sm font-bold text-slate-500 uppercase tracking-wider">{t.loading}</p>
                        </div>
                    </div>
                ) : (
                    <div className="flex-1 overflow-y-auto custom-scrollbar">
                        <table className="w-full text-left border-collapse">
                            <thead className={`sticky top-0 z-10 text-[10px] uppercase font-black tracking-[0.15em] ${isDarkMode ? 'bg-slate-800 text-slate-400' : 'bg-slate-50 text-slate-500'}`}>
                                <tr>
                                    <th className="px-6 py-4">{t.id}</th>
                                    <th className="px-6 py-4">{t.employee}</th>
                                    <th className="px-6 py-4">{t.amount}</th>
                                    <th className="px-6 py-4">{t.date}</th>
                                    <th className="px-6 py-4">{t.createdAt}</th>
                                    <th className="px-6 py-4 text-right">{t.actions}</th>
                                </tr>
                            </thead>
                            <tbody className={`divide-y text-xs ${isDarkMode ? 'divide-slate-800' : 'divide-slate-100'}`}>
                                {filteredDividends.length === 0 ? (
                                    <tr>
                                        <td colSpan="6" className="px-6 py-32 text-center">
                                            <div className="flex flex-col items-center opacity-20">
                                                <AlertCircle size={48} className="mb-2" />
                                                <p className="text-sm font-black uppercase tracking-widest">{t.noData}</p>
                                            </div>
                                        </td>
                                    </tr>
                                ) : (
                                    filteredDividends.map((dividend) => (
                                        <tr key={dividend.DividendID} className="hover:bg-blue-600/5 transition-all group">
                                            <td className="px-6 py-4 font-mono text-[10px] opacity-40 font-bold">
                                                #{dividend.DividendID}
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-3">
                                                    <div className="w-10 h-10 rounded-xl flex items-center justify-center font-black text-white bg-gradient-to-br from-blue-500 to-indigo-600 shadow-inner">
                                                        {dividend.EmployeeName?.charAt(0).toUpperCase() || 'N'}
                                                    </div>
                                                    <div>
                                                        <p className="font-bold text-sm">{dividend.EmployeeName || 'N/A'}</p>
                                                        <p className="text-[10px] opacity-50">ID: {dividend.EmployeeID}</p>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <span className="font-black text-sm text-green-600">
                                                    {formatCurrency(dividend.DividendAmount)}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 text-sm">
                                                {new Date(dividend.DividendDate).toLocaleDateString(language === 'vi' ? 'vi-VN' : 'en-US')}
                                            </td>
                                            <td className={`px-6 py-4 text-sm ${isDarkMode ? 'text-slate-400' : 'text-gray-500'}`}>
                                                {dividend.CreatedAt ? new Date(dividend.CreatedAt).toLocaleString(language === 'vi' ? 'vi-VN' : 'en-US') : '-'}
                                            </td>
                                            <td className="px-6 py-4 text-right">
                                                <div className="flex justify-end gap-1 opacity-0 group-hover:opacity-100 transition-all">
                                                    <button
                                                        onClick={() => handleEdit(dividend)}
                                                        className={`p-2.5 rounded-xl transition-colors ${isDarkMode ? 'hover:bg-blue-500/20 text-slate-400 hover:text-blue-400' : 'hover:bg-blue-50 text-slate-400 hover:text-blue-600'}`}
                                                    >
                                                        <Edit3 size={15} />
                                                    </button>
                                                    <button
                                                        onClick={() => handleDelete(dividend.DividendID)}
                                                        className={`p-2.5 rounded-xl transition-colors ${isDarkMode ? 'hover:bg-red-500/20 text-slate-400 hover:text-red-400' : 'hover:bg-red-50 text-slate-400 hover:text-red-500'}`}
                                                    >
                                                        <Trash2 size={15} />
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            {/* Modal */}
            {showModal && (
                <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 animate-in fade-in duration-200">
                    <div className="absolute inset-0 bg-slate-950/80 backdrop-blur-md" onClick={() => { setShowModal(false); resetForm(); }} />
                    <div className={`relative w-full max-w-md rounded-[2.5rem] shadow-2xl border p-8 animate-in zoom-in-95 duration-300 ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'}`}>

                        <div className="flex justify-between items-start mb-8">
                            <div>
                                <h3 className="text-2xl font-black uppercase tracking-tighter leading-none mb-2">
                                    {editingDividend ? t.updateTitle : t.createTitle}
                                </h3>
                                <p className="text-[10px] font-bold text-blue-500 uppercase tracking-[0.2em]">
                                    {t.title}
                                </p>
                            </div>
                            <button
                                onClick={() => { setShowModal(false); resetForm(); }}
                                className={`p-2 rounded-full transition-colors ${isDarkMode ? 'hover:bg-slate-800' : 'hover:bg-slate-100'}`}
                            >
                                <X size={24} />
                            </button>
                        </div>

                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div className="space-y-3">
                                <label className="text-[10px] font-black uppercase tracking-widest opacity-40 ml-1">
                                    {t.employeeId} *
                                </label>
                                <input
                                    type="number"
                                    required
                                    value={formData.employee_id}
                                    onChange={(e) => setFormData({ ...formData, employee_id: e.target.value })}
                                    className={`w-full px-6 py-4 rounded-2xl border-2 outline-none transition-all font-bold text-lg ${isDarkMode ? 'bg-slate-950 border-slate-800 focus:border-blue-600' : 'bg-slate-50 border-slate-100 focus:border-blue-500 focus:bg-white'}`}
                                    placeholder="1"
                                />
                            </div>

                            <div className="space-y-3">
                                <label className="text-[10px] font-black uppercase tracking-widest opacity-40 ml-1">
                                    {t.amountVnd} *
                                </label>
                                <input
                                    type="number"
                                    required
                                    value={formData.amount}
                                    onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                                    className={`w-full px-6 py-4 rounded-2xl border-2 outline-none transition-all font-bold text-lg ${isDarkMode ? 'bg-slate-950 border-slate-800 focus:border-blue-600' : 'bg-slate-50 border-slate-100 focus:border-blue-500 focus:bg-white'}`}
                                    placeholder="5000000"
                                />
                            </div>

                            <div className="space-y-3">
                                <label className="text-[10px] font-black uppercase tracking-widest opacity-40 ml-1">
                                    {t.issueDate} *
                                </label>
                                <input
                                    type="date"
                                    required
                                    value={formData.date}
                                    onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                                    className={`w-full px-6 py-4 rounded-2xl border-2 outline-none transition-all font-bold text-sm ${isDarkMode ? 'bg-slate-950 border-slate-800 focus:border-blue-600' : 'bg-slate-50 border-slate-100 focus:border-blue-500 focus:bg-white'}`}
                                />
                            </div>

                            <div className="flex gap-4 pt-4">
                                <button
                                    type="submit"
                                    disabled={isSubmitting}
                                    className="flex-1 py-4 rounded-2xl font-black text-xs uppercase tracking-[0.2em] bg-blue-600 hover:bg-blue-700 text-white shadow-xl shadow-blue-500/30 transition-all flex items-center justify-center gap-3 disabled:opacity-50"
                                >
                                    {isSubmitting ? (
                                        <Loader2 size={18} className="animate-spin" />
                                    ) : (
                                        <CheckCircle2 size={18} strokeWidth={3} />
                                    )}
                                    {editingDividend ? t.update : t.create}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default DividendsPage;
