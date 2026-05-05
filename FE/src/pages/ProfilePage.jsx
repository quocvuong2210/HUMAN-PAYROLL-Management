import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useOutletContext, useNavigate } from 'react-router-dom';
import {
  User, Mail, Phone, Calendar, Shield, Key, Edit3, Save, X,
  CheckCircle2, AlertCircle, Loader2, Clock, MapPin, Monitor,
  Eye, EyeOff, LogOut, Activity, Award, Briefcase, History
} from 'lucide-react';
import { formatDateForInput } from '../utils/dateHelpers';

const API_BASE = `${import.meta.env.VITE_API_URL}/api/v1/auth`;

export default function ProfilePage() {
  const { isDarkMode, language } = useOutletContext();
  const navigate = useNavigate();

  // States
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [profile, setProfile] = useState(null);
  const [accessLogs, setAccessLogs] = useState([]);
  const [isEditMode, setIsEditMode] = useState(false);
  const [isChangePasswordMode, setIsChangePasswordMode] = useState(false);
  const [showOldPassword, setShowOldPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [toast, setToast] = useState({ show: false, message: '', type: 'success' });
  const [showLogoutModal, setShowLogoutModal] = useState(false);

  // Form data
  const [formData, setFormData] = useState({
    email: '',
    phone: '',
    dob: '',
    gender: 'Nam'
  });

  // Password form
  const [passwordForm, setPasswordForm] = useState({
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  // Language
  const t = {
    vi: {
      title: "Hồ Sơ Cá Nhân",
      subtitle: "Quản lý thông tin và bảo mật tài khoản",
      info: "Thông tin cá nhân",
      security: "Bảo mật",
      activity: "Hoạt động gần đây",
      edit: "Chỉnh sửa",
      save: "Lưu thay đổi",
      cancel: "Hủy",
      changePassword: "Đổi mật khẩu",
      oldPassword: "Mật khẩu cũ",
      newPassword: "Mật khẩu mới",
      confirmPassword: "Xác nhận mật khẩu",
      logout: "Đăng xuất",
      roles: "Vai trò",
      permissions: "Quyền hạn",
      functions: "Chức năng",
      lastLogin: "Đăng nhập gần nhất",
      accountStatus: "Trạng thái tài khoản",
      memberSince: "Thành viên từ",
      noLogs: "Chưa có lịch sử truy cập",
      loading: "Đang tải...",
      saving: "Đang lưu...",
      success: "Thành công!",
      error: "Có lỗi xảy ra!",
      passwordMismatch: "Mật khẩu xác nhận không khớp",
      passwordTooShort: "Mật khẩu phải có ít nhất 6 ký tự"
    },
    en: {
      title: "Profile",
      subtitle: "Manage your account information and security",
      info: "Personal Information",
      security: "Security",
      activity: "Recent Activity",
      edit: "Edit",
      save: "Save Changes",
      cancel: "Cancel",
      changePassword: "Change Password",
      oldPassword: "Old Password",
      newPassword: "New Password",
      confirmPassword: "Confirm Password",
      logout: "Logout",
      roles: "Roles",
      permissions: "Permissions",
      functions: "Functions",
      lastLogin: "Last Login",
      accountStatus: "Account Status",
      memberSince: "Member Since",
      noLogs: "No access logs yet",
      loading: "Loading...",
      saving: "Saving...",
      success: "Success!",
      error: "Error occurred!",
      passwordMismatch: "Passwords do not match",
      passwordTooShort: "Password must be at least 6 characters"
    }
  }[language || 'vi'];

  const showToast = (message, type = 'success') => {
    setToast({ show: true, message, type });
    setTimeout(() => setToast(prev => ({ ...prev, show: false })), 3000);
  };

  // Fetch profile
  const fetchProfile = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('accessToken') || localStorage.getItem('access_token') || localStorage.getItem('token');
      const res = await axios.get(`${API_BASE}/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (res.data.status === 'success') {
        console.log('📝 Profile data from API:', res.data.data);
        console.log('📅 DateOfBirth (dob) from API:', res.data.data.dob);

        setProfile(res.data.data);

        const formattedData = {
          email: res.data.data.email || '',
          phone: res.data.data.phone || '',
          dob: formatDateForInput(res.data.data.dob),
          gender: res.data.data.gender || 'Nam'
        };

        console.log('✅ Formatted dob:', formattedData.dob);

        setFormData(formattedData);
      }
    } catch (err) {
      showToast(t.error, 'error');
    } finally {
      setLoading(false);
    }
  };

  // Fetch access logs
  const fetchAccessLogs = async () => {
    try {
      const token = localStorage.getItem('accessToken') || localStorage.getItem('access_token') || localStorage.getItem('token');
      const res = await axios.get(`${API_BASE}/my-access-logs?limit=10`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (res.data.status === 'success') {
        setAccessLogs(res.data.data || []);
      }
    } catch (err) {
      console.error('Error fetching access logs:', err);
    }
  };

  useEffect(() => {
    fetchProfile();
    fetchAccessLogs();
  }, []);

  // Update profile
  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    setActionLoading(true);

    try {
      const token = localStorage.getItem('accessToken') || localStorage.getItem('access_token') || localStorage.getItem('token');
      const res = await axios.put(`${API_BASE}/profile`, formData, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (res.data.status === 'success') {
        setProfile(res.data.data);
        setIsEditMode(false);
        showToast('Cập nhật profile thành công!', 'success');
      } else {
        showToast(res.data.message, 'error');
      }
    } catch (err) {
      showToast(err.response?.data?.message || t.error, 'error');
    } finally {
      setActionLoading(false);
    }
  };

  // Change password
  const handleChangePassword = async (e) => {
    e.preventDefault();

    // Validation
    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      showToast(t.passwordMismatch, 'error');
      return;
    }

    if (passwordForm.newPassword.length < 6) {
      showToast(t.passwordTooShort, 'error');
      return;
    }

    setActionLoading(true);

    try {
      const token = localStorage.getItem('accessToken') || localStorage.getItem('access_token') || localStorage.getItem('token');
      const res = await axios.post(`${API_BASE}/change-password`, {
        oldPassword: passwordForm.oldPassword,
        newPassword: passwordForm.newPassword
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (res.data.status === 'success') {
        setIsChangePasswordMode(false);
        setPasswordForm({ oldPassword: '', newPassword: '', confirmPassword: '' });
        showToast('Đổi mật khẩu thành công!', 'success');
      } else {
        showToast(res.data.message, 'error');
      }
    } catch (err) {
      showToast(err.response?.data?.message || t.error, 'error');
    } finally {
      setActionLoading(false);
    }
  };

  // Logout
  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('access_token');
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('roles');
    localStorage.removeItem('user_roles');
    localStorage.removeItem('user_permissions');
    localStorage.removeItem('user_functions');
    localStorage.removeItem('user_info');
    navigate('/login');
  };

  // Get action icon and color
  const getActionStyle = (action) => {
    if (action?.includes('SUCCESS')) return { icon: CheckCircle2, color: 'text-green-500', bg: 'bg-green-500/10' };
    if (action?.includes('FAILED')) return { icon: AlertCircle, color: 'text-red-500', bg: 'bg-red-500/10' };
    return { icon: Activity, color: 'text-blue-500', bg: 'bg-blue-500/10' };
  };

  if (loading) {
    return (
      <div className={`w-full h-full flex items-center justify-center ${isDarkMode ? 'bg-slate-950' : 'bg-slate-50'}`}>
        <Loader2 className="animate-spin text-blue-500" size={48} />
      </div>
    );
  }

  return (
    <div className={`relative w-full h-full p-6 overflow-y-auto custom-scrollbar ${isDarkMode ? 'text-slate-300 bg-slate-950' : 'text-slate-800 bg-slate-50'}`}>

      {/* TOAST */}
      {toast.show && (
        <div className={`fixed top-6 left-1/2 -translate-x-1/2 z-[100] flex items-center gap-3 px-6 py-3 rounded-2xl shadow-2xl animate-in fade-in slide-in-from-top-5 duration-300 ${toast.type === 'success' ? 'bg-emerald-500 text-white' : 'bg-red-500 text-white'}`}>
          {toast.type === 'success' ? <CheckCircle2 size={18} /> : <AlertCircle size={18} />}
          <span className="text-sm font-bold">{toast.message}</span>
        </div>
      )}

      {/* HEADER */}
      <div className="mb-4">
        <h1 className="text-xl font-black uppercase border-l-4 border-blue-600 pl-3 leading-none italic">{t.title}</h1>
        <p className="text-xs opacity-60 mt-1.5 ml-4">{t.subtitle}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">

        {/* LEFT COLUMN - Profile Info */}
        <div className="lg:col-span-2 space-y-4">

          {/* Profile Card */}
          <div className={`rounded-xl border overflow-hidden ${isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
            {/* Header with Avatar */}
            <div className="relative h-24 bg-gradient-to-r from-blue-600 to-indigo-600">
              <div className="absolute -bottom-10 left-6">
                <div className="w-20 h-20 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-700 flex items-center justify-center text-3xl font-black text-white shadow-2xl border-4 border-slate-900">
                  {profile?.username?.charAt(0).toUpperCase()}
                </div>
              </div>
            </div>

            {/* Profile Info */}
            <div className="pt-14 px-6 pb-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h2 className="text-xl font-black">{profile?.username}</h2>
                  <p className="text-xs opacity-60 flex items-center gap-1.5 mt-1">
                    <Mail size={12} /> {profile?.email}
                  </p>
                </div>

                {!isEditMode && !isChangePasswordMode && (
                  <button
                    onClick={() => setIsEditMode(true)}
                    className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-bold transition-all shadow-lg shadow-blue-600/20"
                  >
                    <Edit3 size={14} /> {t.edit}
                  </button>
                )}
              </div>

              {/* Roles Badges */}
              <div className="flex flex-wrap gap-1.5 mb-4">
                {profile?.roles?.map((role, idx) => (
                  <span key={idx} className="px-2 py-0.5 bg-blue-500/10 text-blue-500 rounded-full text-[10px] font-bold flex items-center gap-1">
                    <Shield size={10} /> {role.RoleName}
                  </span>
                ))}
              </div>

              {/* Edit Form */}
              {isEditMode ? (
                <form onSubmit={handleUpdateProfile} className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-xs font-bold uppercase opacity-50 mb-2 block">Email</label>
                      <input
                        type="email"
                        value={formData.email}
                        onChange={e => setFormData({ ...formData, email: e.target.value })}
                        className={`w-full p-3 rounded-xl border text-sm ${isDarkMode ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'}`}
                      />
                    </div>
                    <div>
                      <label className="text-xs font-bold uppercase opacity-50 mb-2 block">Số điện thoại</label>
                      <input
                        type="tel"
                        value={formData.phone}
                        onChange={e => setFormData({ ...formData, phone: e.target.value })}
                        className={`w-full p-3 rounded-xl border text-sm ${isDarkMode ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'}`}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-xs font-bold uppercase opacity-50 mb-2 block">Ngày sinh</label>
                      <input
                        type="date"
                        value={formData.dob}
                        onChange={e => setFormData({ ...formData, dob: e.target.value })}
                        className={`w-full p-3 rounded-xl border text-sm ${isDarkMode ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'}`}
                      />
                    </div>
                    <div>
                      <label className="text-xs font-bold uppercase opacity-50 mb-2 block">Giới tính</label>
                      <select
                        value={formData.gender}
                        onChange={e => setFormData({ ...formData, gender: e.target.value })}
                        className={`w-full p-3 rounded-xl border text-sm ${isDarkMode ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'}`}
                      >
                        <option value="Nam">Nam</option>
                        <option value="Nữ">Nữ</option>
                        <option value="Khác">Khác</option>
                      </select>
                    </div>
                  </div>

                  <div className="flex gap-3 pt-4">
                    <button
                      type="submit"
                      disabled={actionLoading}
                      className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-xl font-bold transition-all"
                    >
                      {actionLoading ? <Loader2 className="animate-spin" size={18} /> : <Save size={18} />}
                      {actionLoading ? t.saving : t.save}
                    </button>
                    <button
                      type="button"
                      onClick={() => setIsEditMode(false)}
                      className="px-4 py-3 bg-slate-500/10 hover:bg-slate-500/20 rounded-xl font-bold transition-all"
                    >
                      {t.cancel}
                    </button>
                  </div>
                </form>
              ) : (
                <div className="grid grid-cols-2 gap-4">
                  <div className={`p-4 rounded-xl ${isDarkMode ? 'bg-slate-800/50' : 'bg-slate-50'}`}>
                    <p className="text-xs font-bold uppercase opacity-50 mb-1">Số điện thoại</p>
                    <p className="font-bold flex items-center gap-2">
                      <Phone size={16} className="opacity-50" />
                      {profile?.phone || 'Chưa cập nhật'}
                    </p>
                  </div>
                  <div className={`p-4 rounded-xl ${isDarkMode ? 'bg-slate-800/50' : 'bg-slate-50'}`}>
                    <p className="text-xs font-bold uppercase opacity-50 mb-1">Ngày sinh</p>
                    <p className="font-bold flex items-center gap-2">
                      <Calendar size={16} className="opacity-50" />
                      {profile?.dob ? new Date(profile.dob).toLocaleDateString('vi-VN') : 'Chưa cập nhật'}
                    </p>
                  </div>
                  <div className={`p-4 rounded-xl ${isDarkMode ? 'bg-slate-800/50' : 'bg-slate-50'}`}>
                    <p className="text-xs font-bold uppercase opacity-50 mb-1">Giới tính</p>
                    <p className="font-bold">{profile?.gender || 'Chưa cập nhật'}</p>
                  </div>
                  <div className={`p-4 rounded-xl ${isDarkMode ? 'bg-slate-800/50' : 'bg-slate-50'}`}>
                    <p className="text-xs font-bold uppercase opacity-50 mb-1">Trạng thái</p>
                    <p className="font-bold text-green-500">{profile?.status}</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Change Password Card */}
          <div className={`rounded-xl border overflow-hidden ${isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
            <div className="p-4 border-b border-slate-800/10 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="p-1.5 bg-amber-500/10 text-amber-500 rounded-lg">
                  <Key size={16} />
                </div>
                <div>
                  <h3 className="font-black uppercase text-xs">{t.security}</h3>
                  <p className="text-[10px] opacity-60">Quản lý mật khẩu và bảo mật</p>
                </div>
              </div>

              {!isChangePasswordMode && !isEditMode && (
                <button
                  onClick={() => setIsChangePasswordMode(true)}
                  className="px-3 py-1.5 bg-amber-500/10 hover:bg-amber-500/20 text-amber-500 rounded-lg text-xs font-bold transition-all"
                >
                  {t.changePassword}
                </button>
              )}
            </div>

            {isChangePasswordMode ? (
              <form onSubmit={handleChangePassword} className="p-6 space-y-4">
                <div>
                  <label className="text-xs font-bold uppercase opacity-50 mb-2 block">{t.oldPassword}</label>
                  <div className="relative">
                    <input
                      type={showOldPassword ? 'text' : 'password'}
                      value={passwordForm.oldPassword}
                      onChange={e => setPasswordForm({ ...passwordForm, oldPassword: e.target.value })}
                      required
                      className={`w-full p-3 pr-12 rounded-xl border text-sm ${isDarkMode ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'}`}
                    />
                    <button
                      type="button"
                      onClick={() => setShowOldPassword(!showOldPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 opacity-50 hover:opacity-100"
                    >
                      {showOldPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                </div>

                <div>
                  <label className="text-xs font-bold uppercase opacity-50 mb-2 block">{t.newPassword}</label>
                  <div className="relative">
                    <input
                      type={showNewPassword ? 'text' : 'password'}
                      value={passwordForm.newPassword}
                      onChange={e => setPasswordForm({ ...passwordForm, newPassword: e.target.value })}
                      required
                      minLength={6}
                      className={`w-full p-3 pr-12 rounded-xl border text-sm ${isDarkMode ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'}`}
                    />
                    <button
                      type="button"
                      onClick={() => setShowNewPassword(!showNewPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 opacity-50 hover:opacity-100"
                    >
                      {showNewPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                </div>

                <div>
                  <label className="text-xs font-bold uppercase opacity-50 mb-2 block">{t.confirmPassword}</label>
                  <input
                    type="password"
                    value={passwordForm.confirmPassword}
                    onChange={e => setPasswordForm({ ...passwordForm, confirmPassword: e.target.value })}
                    required
                    className={`w-full p-3 rounded-xl border text-sm ${isDarkMode ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'}`}
                  />
                </div>

                <div className="flex gap-3 pt-4">
                  <button
                    type="submit"
                    disabled={actionLoading}
                    className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-amber-600 hover:bg-amber-700 disabled:bg-amber-400 text-white rounded-xl font-bold transition-all"
                  >
                    {actionLoading ? <Loader2 className="animate-spin" size={18} /> : <Key size={18} />}
                    {actionLoading ? t.saving : t.changePassword}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setIsChangePasswordMode(false);
                      setPasswordForm({ oldPassword: '', newPassword: '', confirmPassword: '' });
                    }}
                    className="px-4 py-3 bg-slate-500/10 hover:bg-slate-500/20 rounded-xl font-bold transition-all"
                  >
                    {t.cancel}
                  </button>
                </div>
              </form>
            ) : (
              <div className="p-6">
                <p className="text-sm opacity-60">Mật khẩu của bạn được mã hóa an toàn. Đổi mật khẩu định kỳ để bảo vệ tài khoản.</p>
              </div>
            )}
          </div>
        </div>

        {/* RIGHT COLUMN - Activity & Stats */}
        <div className="space-y-4">

          {/* Account Stats */}
          <div className={`rounded-xl border p-4 ${isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
            <h3 className="font-black uppercase text-xs mb-3 flex items-center gap-1.5">
              <Award size={14} className="text-blue-500" />
              Thông tin tài khoản
            </h3>

            <div className="space-y-2">
              <div className="flex items-center justify-between py-1.5 border-b border-slate-800/10">
                <span className="text-[10px] opacity-60">Thành viên từ</span>
                <span className="text-xs font-bold">
                  {profile?.createdAt ? new Date(profile.createdAt).toLocaleDateString('vi-VN') : 'N/A'}
                </span>
              </div>
              <div className="flex items-center justify-between py-1.5 border-b border-slate-800/10">
                <span className="text-[10px] opacity-60">Số vai trò</span>
                <span className="text-xs font-bold text-blue-500">{profile?.roles?.length || 0}</span>
              </div>
              <div className="flex items-center justify-between py-1.5 border-b border-slate-800/10">
                <span className="text-[10px] opacity-60">Số quyền hạn</span>
                <span className="text-xs font-bold text-green-500">{profile?.permissions?.length || 0}</span>
              </div>
              <div className="flex items-center justify-between py-1.5">
                <span className="text-[10px] opacity-60">Số chức năng</span>
                <span className="text-xs font-bold text-purple-500">{profile?.functions?.length || 0}</span>
              </div>
            </div>
          </div>

          {/* Access Logs */}
          <div className={`rounded-xl border overflow-hidden ${isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
            <div className="p-4 border-b border-slate-800/10">
              <h3 className="font-black uppercase text-xs flex items-center gap-1.5">
                <History size={14} className="text-emerald-500" />
                {t.activity}
              </h3>
            </div>

            <div className="p-3 space-y-1.5 max-h-80 overflow-y-auto custom-scrollbar">
              {accessLogs.length === 0 ? (
                <p className="text-center text-xs opacity-60 py-6">{t.noLogs}</p>
              ) : (
                accessLogs.map((log) => {
                  const style = getActionStyle(log.Action);
                  const Icon = style.icon;

                  return (
                    <div key={log.LogID} className={`p-2.5 rounded-lg ${isDarkMode ? 'bg-slate-800/50' : 'bg-slate-50'}`}>
                      <div className="flex items-start gap-2">
                        <div className={`p-1.5 rounded-lg ${style.bg}`}>
                          <Icon size={12} className={style.color} />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-[10px] font-bold">{log.Action}</p>
                          <p className="text-[10px] opacity-60 flex items-center gap-1 mt-0.5">
                            <Clock size={8} />
                            {new Date(log.AccessTime).toLocaleString('vi-VN')}
                          </p>
                          <p className="text-[10px] opacity-60 flex items-center gap-1 mt-0.5">
                            <MapPin size={8} />
                            {log.IPAddress}
                          </p>
                        </div>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>

          {/* Logout Button */}
          <button
            onClick={() => setShowLogoutModal(true)}
            className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-red-600 hover:bg-red-700 text-white rounded-lg font-bold transition-all shadow-lg shadow-red-600/20 text-sm"
          >
            <LogOut size={16} />
            {t.logout}
          </button>
        </div>
      </div>

      {/* LOGOUT CONFIRMATION MODAL */}
      {showLogoutModal && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-sm animate-in fade-in">
          <div className={`w-full max-w-sm rounded-2xl overflow-hidden shadow-2xl animate-in zoom-in-95 ${isDarkMode ? 'bg-slate-900 border border-slate-800' : 'bg-white'}`}>
            <div className="p-6 text-center">
              <div className="mx-auto w-14 h-14 bg-red-500/10 text-red-500 rounded-full flex items-center justify-center mb-3">
                <LogOut size={24} />
              </div>
              <h3 className="text-base font-black mb-2 uppercase italic tracking-tight">Xác nhận đăng xuất?</h3>
              <p className="text-xs opacity-60 leading-relaxed">Bạn có chắc chắn muốn đăng xuất khỏi hệ thống?</p>
            </div>
            <div className="flex border-t border-slate-800/10">
              <button
                onClick={() => setShowLogoutModal(false)}
                className="flex-1 py-3 text-xs font-bold uppercase hover:bg-slate-500/5 transition-colors"
              >
                Hủy
              </button>
              <button
                onClick={handleLogout}
                className="flex-1 py-3 text-xs font-bold uppercase bg-red-600 text-white hover:bg-red-700 transition-colors"
              >
                Đăng xuất
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
