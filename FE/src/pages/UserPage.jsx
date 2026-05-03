import React, { useState, useEffect, useCallback } from 'react'
import { useOutletContext } from 'react-router-dom'
import { 
  Users, UserPlus, Search, Edit2, Trash2, X, 
  Loader2, ChevronRight, CheckCircle2, Clock, Globe, 
  Monitor, AlertCircle, RefreshCw, Calendar, Mail, Phone, User,
  Shield, ChevronLeft, ChevronsLeft, ChevronsRight
} from 'lucide-react'

const API_BASE = import.meta.env.VITE_API_URL

const translations = {
  vi: {
    title: 'Quản Lý Người Dùng',
    addUser: 'Thêm Người Dùng',
    searchPlaceholder: 'Tìm kiếm người dùng...',
    users: 'Danh Sách',
    accessLogs: 'Lịch Sử Truy Cập',
    userDetails: 'Chi Tiết Người Dùng',
    edit: 'Chỉnh Sửa',
    delete: 'Xóa',
    save: 'Lưu',
    cancel: 'Hủy',
    username: 'Tên Đăng Nhập',
    email: 'Email',
    phone: 'Số Điện Thoại',
    dob: 'Ngày Sinh',
    gender: 'Giới Tính',
    status: 'Trạng Thái',
    createdAt: 'Ngày Tạo',
    action: 'Hành Động',
    ipAddress: 'Địa Chỉ IP',
    userAgent: 'Thiết Bị',
    time: 'Thời Gian',
    noData: 'Không có dữ liệu',
    confirmDelete: 'Bạn chắc chắn muốn xóa tài khoản này?',
    password: 'Mật Khẩu',
    male: 'Nam',
    female: 'Nữ',
    active: 'Hoạt Động',
    inactive: 'Đã Khóa',
    loginSuccess: 'Thành Công',
    loginFailed: 'Thất Bại',
    refresh: 'Làm Mới',
    loading: 'Đang tải...',
    totalUsers: 'Tổng Người Dùng',
    activeUsers: 'Đang Hoạt Động',
    todayLogins: 'Đăng Nhập Hôm Nay',
    failedLogins: 'Đăng Nhập Thất Bại',
    results: 'kết quả',
    createUser: 'Tạo Người Dùng',
    updateUser: 'Cập Nhật Người Dùng'
  },
  en: {
    title: 'User Management',
    addUser: 'Add User',
    searchPlaceholder: 'Search users...',
    users: 'User List',
    accessLogs: 'Access Logs',
    userDetails: 'User Details',
    edit: 'Edit',
    delete: 'Delete',
    save: 'Save',
    cancel: 'Cancel',
    username: 'Username',
    email: 'Email',
    phone: 'Phone Number',
    dob: 'Date of Birth',
    gender: 'Gender',
    status: 'Status',
    createdAt: 'Created At',
    action: 'Action',
    ipAddress: 'IP Address',
    userAgent: 'Device',
    time: 'Time',
    noData: 'No data',
    confirmDelete: 'Are you sure you want to delete this account?',
    password: 'Password',
    male: 'Male',
    female: 'Female',
    active: 'Active',
    inactive: 'Inactive',
    loginSuccess: 'Success',
    loginFailed: 'Failed',
    refresh: 'Refresh',
    loading: 'Loading...',
    totalUsers: 'Total Users',
    activeUsers: 'Active Users',
    todayLogins: 'Today Logins',
    failedLogins: 'Failed Logins',
    results: 'results',
    createUser: 'Create User',
    updateUser: 'Update User'
  }
}

export default function UserPage() {
  const { isDarkMode, language } = useOutletContext() || { isDarkMode: false, language: 'vi' }
  const lang = language || 'vi'
  const t = translations[lang]

  const [users, setUsers] = useState([])
  const [accessLogs, setAccessLogs] = useState([])
  const [loading, setLoading] = useState(false)
  const [logsLoading, setLogsLoading] = useState(false)
  const [selectedUser, setSelectedUser] = useState(null)
  const [showModal, setShowModal] = useState(false)
  const [showEditModal, setShowEditModal] = useState(false)
  const [activeTab, setActiveTab] = useState('users')
  const [searchTerm, setSearchTerm] = useState('')
  
  const [editForm, setEditForm] = useState({
    username: '',
    email: '',
    phone: '',
    dob: '',
    gender: '',
    status: ''
  })
  
  const [newUserForm, setNewUserForm] = useState({
    username: '',
    email: '',
    password: '',
    phone: '',
    dob: '',
    gender: 'Nam'
  })

  const fetchUsers = useCallback(async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/api/v1/auth/admin/users`)
      const data = await res.json()
      setUsers(data.data || [])
    } catch (err) {
      console.error('Error fetching users:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  const fetchAccessLogs = useCallback(async () => {
    setLogsLoading(true)
    try {
      const res = await fetch(`${API_BASE}/api/v1/auth/admin/logs`)
      const data = await res.json()
      setAccessLogs(data.data || [])
    } catch (err) {
      console.error('Error fetching access logs:', err)
    } finally {
      setLogsLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchUsers()
    fetchAccessLogs()
  }, [fetchUsers, fetchAccessLogs])

  const handleDelete = async (id) => {
    if (!window.confirm(t.confirmDelete)) return
    try {
      await fetch(`${API_BASE}/api/v1/auth/users/${id}`, { method: 'DELETE' })
      fetchUsers()
      setSelectedUser(null)
    } catch (err) {
      alert('Error deleting user')
    }
  }

  const handleEdit = (user) => {
    setEditForm({
      username: user.Username || '',
      email: user.Email || '',
      phone: user.PhoneNumber || '',
      dob: user.DateOfBirth?.split('T')[0] || '',
      gender: user.Gender || '',
      status: user.Status || ''
    })
    setShowEditModal(true)
  }

  const handleUpdateUser = async () => {
    if (!selectedUser) return
    try {
      // Convert empty string to null for date fields
      const payload = {
        username: editForm.username || null,
        email: editForm.email || null,
        phone: editForm.phone || null,
        dob: editForm.dob && editForm.dob.trim() !== '' ? editForm.dob : null,
        gender: editForm.gender || null,
        status: editForm.status || null
      }
      
      const res = await fetch(`${API_BASE}/api/v1/auth/users/${selectedUser.UserID}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      const data = await res.json()
      if (data.status === 'success') {
        fetchUsers()
        setShowEditModal(false)
        setSelectedUser(null)
      } else {
        alert(data.message)
      }
    } catch (err) {
      alert('Error updating user')
    }
  }

  const handleCreateUser = async () => {
    try {
      // Convert empty string to null for date fields
      const payload = {
        username: newUserForm.username || null,
        email: newUserForm.email || null,
        password: newUserForm.password || null,
        phone: newUserForm.phone || null,
        dob: newUserForm.dob && newUserForm.dob.trim() !== '' ? newUserForm.dob : null,
        gender: newUserForm.gender || null
      }
      
      const res = await fetch(`${API_BASE}/api/v1/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      const data = await res.json()
      if (data.status === 'success') {
        fetchUsers()
        setShowModal(false)
        setNewUserForm({
          username: '',
          email: '',
          password: '',
          phone: '',
          dob: '',
          gender: 'Nam'
        })
      } else {
        alert(data.message)
      }
    } catch (err) {
      alert('Error creating user')
    }
  }

  const filteredUsers = users.filter(user => 
    user.Username?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.Email?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const filteredLogs = accessLogs.filter(log =>
    log.Username?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    log.Email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    log.Action?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const formatDateTime = (dateStr) => {
    if (!dateStr) return 'N/A'
    const date = new Date(dateStr)
    return date.toLocaleString(lang === 'vi' ? 'vi-VN' : 'en-US')
  }

  // Stats calculations
  const totalUsers = users.length
  const activeUsers = users.filter(u => u.Status === 'ACTIVE').length
  const todayLogins = accessLogs.filter(log => {
    const logDate = new Date(log.AccessTime).toDateString()
    return logDate === new Date().toDateString() && log.Action === 'LOGIN_SUCCESS'
  }).length
  const failedLogins = accessLogs.filter(log => log.Action === 'LOGIN_FAILED').length

  const tabs = [
    { id: 'users', label: t.users, icon: Users },
    { id: 'logs', label: t.accessLogs, icon: Clock }
  ]

  const InfoRow = ({ icon: Icon, label, value }) => (
    <div className="flex items-center gap-3">
      <div className={`p-2 rounded-lg ${isDarkMode ? 'bg-slate-800' : 'bg-slate-100'}`}>
        <Icon size={14} className="text-slate-400" />
      </div>
      <div className="flex-1">
        <p className="text-[10px] text-slate-400 uppercase tracking-wider">{label}</p>
        <p className={`text-sm font-medium ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>{value}</p>
      </div>
    </div>
  )

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
                className={`pb-2 flex items-center gap-2 border-b-2 transition-all duration-200 ${
                  activeTab === tab.id 
                    ? 'border-blue-500 text-blue-500 font-semibold' 
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon size={18} /> {tab.label}
              </button>
            )
          })}
        </div>
        
        <div className="flex items-center gap-3">
          <button 
            onClick={() => { fetchUsers(); fetchAccessLogs(); }}
            disabled={loading || logsLoading}
            className="text-xs px-3 py-1.5 bg-blue-600/10 text-blue-600 rounded-lg flex items-center gap-2 hover:bg-blue-600/20 disabled:opacity-50"
          >
            <RefreshCw size={14} className={(loading || logsLoading) ? 'animate-spin' : ''} />
            {t.refresh}
          </button>
          <button 
            onClick={() => setShowModal(true)} 
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-1.5 rounded-lg font-semibold text-sm flex items-center gap-2 shadow-lg shadow-blue-600/20 transition-all"
          >
            <UserPlus size={16} /> {t.addUser}
          </button>
        </div>
      </div>

      {/* Filter Bar */}
      <div className={`grid grid-cols-2 md:grid-cols-6 gap-3 p-4 rounded-xl border ${
        isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
      }`}>
        <div className="col-span-2 flex items-center gap-2">
          <Search className="text-slate-400" size={18} />
          <input 
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="bg-transparent w-full focus:outline-none text-sm" 
            placeholder={t.searchPlaceholder}
          />
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Total Users */}
        <div className={`p-4 rounded-xl flex items-center justify-between border ${
          isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
        }`}>
          <div>
            <p className="text-[10px] font-bold text-blue-500 uppercase tracking-wide">{t.totalUsers}</p>
            <h3 className={`text-lg font-black mt-1 ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
              {loading ? '...' : totalUsers}
            </h3>
          </div>
          <div className="bg-blue-500/10 p-2.5 rounded-xl">
            <Users size={20} className="text-blue-500" />
          </div>
        </div>

        {/* Active Users */}
        <div className={`p-4 rounded-xl flex items-center justify-between border ${
          isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
        }`}>
          <div>
            <p className="text-[10px] font-bold text-emerald-500 uppercase tracking-wide">{t.activeUsers}</p>
            <h3 className={`text-lg font-black mt-1 ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
              {loading ? '...' : activeUsers}
            </h3>
          </div>
          <div className="bg-emerald-500/10 p-2.5 rounded-xl">
            <CheckCircle2 size={20} className="text-emerald-500" />
          </div>
        </div>

        {/* Today Logins */}
        <div className={`p-4 rounded-xl flex items-center justify-between border ${
          isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
        }`}>
          <div>
            <p className="text-[10px] font-bold text-amber-500 uppercase tracking-wide">{t.todayLogins}</p>
            <h3 className={`text-lg font-black mt-1 ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
              {logsLoading ? '...' : todayLogins}
            </h3>
          </div>
          <div className="bg-amber-500/10 p-2.5 rounded-xl">
            <Shield size={20} className="text-amber-500" />
          </div>
        </div>

        {/* Failed Logins */}
        <div className={`p-4 rounded-xl flex items-center justify-between border ${
          isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
        }`}>
          <div>
            <p className="text-[10px] font-bold text-rose-500 uppercase tracking-wide">{t.failedLogins}</p>
            <h3 className={`text-lg font-black mt-1 ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
              {logsLoading ? '...' : failedLogins}
            </h3>
          </div>
          <div className="bg-rose-500/10 p-2.5 rounded-xl">
            <AlertCircle size={20} className="text-rose-500" />
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex gap-6">
        {/* Table Section */}
        <div className={`flex-1 border overflow-hidden rounded-xl ${
          isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200'
        }`}>
          
          {/* Users Tab */}
          {activeTab === 'users' && (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className={isDarkMode ? 'bg-slate-800' : 'bg-slate-100'}>
                  <tr>
                    <th className="p-4 text-left text-xs font-bold uppercase tracking-wider">{t.username}</th>
                    <th className="p-4 text-left text-xs font-bold uppercase tracking-wider">{t.email}</th>
                    <th className="p-4 text-left text-xs font-bold uppercase tracking-wider">{t.phone}</th>
                    <th className="p-4 text-left text-xs font-bold uppercase tracking-wider">{t.gender}</th>
                    <th className="p-4 text-left text-xs font-bold uppercase tracking-wider">{t.status}</th>
                    <th className="p-4 text-left text-xs font-bold uppercase tracking-wider">{t.createdAt}</th>
                    <th className="p-4 text-center"></th>
                  </tr>
                </thead>
                <tbody className={`divide-y ${isDarkMode ? 'divide-slate-800' : 'divide-slate-100'}`}>
                  {loading ? (
                    <tr>
                      <td colSpan="7" className="text-center p-10">
                        <Loader2 className="animate-spin text-blue-500 mx-auto" size={24} />
                        <p className="mt-2 text-sm opacity-60">{t.loading}</p>
                      </td>
                    </tr>
                  ) : filteredUsers.length === 0 ? (
                    <tr>
                      <td colSpan="7" className="text-center p-10 text-slate-400">{t.noData}</td>
                    </tr>
                  ) : filteredUsers.map(user => (
                    <tr 
                      key={user.UserID} 
                      onClick={() => setSelectedUser(user)}
                      className={`cursor-pointer transition-colors hover:bg-slate-500/5 ${
                        selectedUser?.UserID === user.UserID ? (isDarkMode ? 'bg-blue-900/20' : 'bg-blue-50') : ''
                      }`}
                    >
                      <td className="p-4">
                        <div className="flex items-center gap-3">
                          <div className={`w-9 h-9 rounded-full flex items-center justify-center font-bold text-sm ${
                            isDarkMode ? 'bg-blue-900 text-blue-400' : 'bg-blue-100 text-blue-600'
                          }`}>
                            {user.Username?.[0]?.toUpperCase() || 'U'}
                          </div>
                          <span className="font-semibold">{user.Username}</span>
                        </div>
                      </td>
                      <td className="p-4 text-slate-500">{user.Email}</td>
                      <td className="p-4 text-slate-500">{user.PhoneNumber || 'N/A'}</td>
                      <td className="p-4">{user.Gender || 'N/A'}</td>
                      <td className="p-4">
                        <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                          user.Status === 'ACTIVE' 
                            ? 'bg-emerald-100 text-emerald-600' 
                            : 'bg-rose-100 text-rose-600'
                        }`}>
                          {user.Status === 'ACTIVE' ? t.active : t.inactive}
                        </span>
                      </td>
                      <td className="p-4 text-slate-500">{formatDateTime(user.CreatedAt)}</td>
                      <td className="p-4 text-center">
                        <ChevronRight className="inline text-slate-300" size={18} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Access Logs Tab */}
          {activeTab === 'logs' && (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className={isDarkMode ? 'bg-slate-800' : 'bg-slate-100'}>
                  <tr>
                    <th className="p-4 text-left text-xs font-bold uppercase tracking-wider">{t.username}</th>
                    <th className="p-4 text-left text-xs font-bold uppercase tracking-wider">{t.email}</th>
                    <th className="p-4 text-left text-xs font-bold uppercase tracking-wider">{t.action}</th>
                    <th className="p-4 text-left text-xs font-bold uppercase tracking-wider">{t.ipAddress}</th>
                    <th className="p-4 text-left text-xs font-bold uppercase tracking-wider">{t.userAgent}</th>
                    <th className="p-4 text-left text-xs font-bold uppercase tracking-wider">{t.time}</th>
                  </tr>
                </thead>
                <tbody className={`divide-y ${isDarkMode ? 'divide-slate-800' : 'divide-slate-100'}`}>
                  {logsLoading ? (
                    <tr>
                      <td colSpan="6" className="text-center p-10">
                        <Loader2 className="animate-spin text-blue-500 mx-auto" size={24} />
                        <p className="mt-2 text-sm opacity-60">{t.loading}</p>
                      </td>
                    </tr>
                  ) : filteredLogs.length === 0 ? (
                    <tr>
                      <td colSpan="6" className="text-center p-10 text-slate-400">{t.noData}</td>
                    </tr>
                  ) : filteredLogs.map((log, idx) => (
                    <tr 
                      key={log.LogID || idx}
                      className="transition-colors hover:bg-slate-500/5"
                    >
                      <td className="p-4">
                        <div className="flex items-center gap-3">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs ${
                            isDarkMode ? 'bg-slate-800 text-slate-400' : 'bg-slate-100 text-slate-600'
                          }`}>
                            {log.Username?.[0]?.toUpperCase() || 'U'}
                          </div>
                          <span className="font-medium">{log.Username}</span>
                        </div>
                      </td>
                      <td className="p-4 text-slate-500">{log.Email}</td>
                      <td className="p-4">
                        <span className={`px-2.5 py-1 rounded-full text-xs font-semibold flex items-center gap-1.5 w-fit ${
                          log.Action === 'LOGIN_SUCCESS' 
                            ? 'bg-emerald-100 text-emerald-600' 
                            : 'bg-rose-100 text-rose-600'
                        }`}>
                          {log.Action === 'LOGIN_SUCCESS' ? (
                            <><CheckCircle2 size={12} /> {t.loginSuccess}</>
                          ) : (
                            <><AlertCircle size={12} /> {t.loginFailed}</>
                          )}
                        </span>
                      </td>
                      <td className="p-4">
                        <div className="flex items-center gap-2 text-slate-500">
                          <Globe size={14} />
                          {log.IPAddress}
                        </div>
                      </td>
                      <td className="p-4">
                        <div className="flex items-center gap-2 text-slate-500 max-w-[200px] truncate">
                          <Monitor size={14} className="flex-shrink-0" />
                          <span className="truncate">{log.UserAgent || 'N/A'}</span>
                        </div>
                      </td>
                      <td className="p-4">
                        <div className="flex items-center gap-2 text-slate-500">
                          <Clock size={14} />
                          {formatDateTime(log.AccessTime)}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Sidebar Detail - Only show when user is selected */}
        {selectedUser && activeTab === 'users' && (
          <div className={`w-[350px] rounded-xl border p-6 flex flex-col gap-5 ${
            isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
          }`}>
            <div className="flex justify-between items-center">
              <h3 className="font-bold text-sm uppercase tracking-wider text-slate-500">{t.userDetails}</h3>
              <button 
                onClick={() => setSelectedUser(null)} 
                className={`p-2 rounded-full ${isDarkMode ? 'hover:bg-slate-800' : 'hover:bg-slate-100'}`}
              >
                <X size={16} />
              </button>
            </div>
            
            <div className="space-y-4">
              <div className="text-center space-y-2">
                <div className={`w-16 h-16 rounded-2xl mx-auto flex items-center justify-center text-xl font-bold ${
                  isDarkMode ? 'bg-blue-900 text-blue-400' : 'bg-blue-600 text-white'
                }`}>
                  {selectedUser.Username?.[0]?.toUpperCase() || 'U'}
                </div>
                <h2 className={`text-lg font-bold ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>{selectedUser.Username}</h2>
                <span className={`px-2.5 py-1 rounded-full text-xs font-semibold inline-block ${
                  selectedUser.Status === 'ACTIVE' 
                    ? 'bg-emerald-100 text-emerald-600' 
                    : 'bg-rose-100 text-rose-600'
                }`}>
                  {selectedUser.Status === 'ACTIVE' ? t.active : t.inactive}
                </span>
              </div>
              
              <div className={`space-y-3 pt-4 border-t ${isDarkMode ? 'border-slate-800' : 'border-slate-100'}`}>
                <InfoRow icon={Mail} label={t.email} value={selectedUser.Email} />
                <InfoRow icon={Phone} label={t.phone} value={selectedUser.PhoneNumber || 'N/A'} />
                <InfoRow icon={Calendar} label={t.dob} value={selectedUser.DateOfBirth?.split('T')[0] || 'N/A'} />
                <InfoRow icon={User} label={t.gender} value={selectedUser.Gender || 'N/A'} />
                <InfoRow icon={Clock} label={t.createdAt} value={formatDateTime(selectedUser.CreatedAt)} />
              </div>
            </div>

            <div className="mt-auto flex gap-3">
              <button 
                onClick={() => handleEdit(selectedUser)}
                className={`flex-1 py-2.5 rounded-xl font-semibold text-sm flex items-center justify-center gap-2 ${
                  isDarkMode ? 'bg-slate-800 hover:bg-slate-700' : 'bg-slate-100 hover:bg-slate-200'
                }`}
              >
                <Edit2 size={14} /> {t.edit}
              </button>
              <button 
                onClick={() => handleDelete(selectedUser.UserID)} 
                className="flex-1 py-2.5 rounded-xl bg-rose-50 text-rose-600 font-semibold text-sm flex items-center justify-center gap-2 hover:bg-rose-100"
              >
                <Trash2 size={14} /> {t.delete}
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Create User Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className={`w-full max-w-md rounded-2xl p-6 ${isDarkMode ? 'bg-slate-900' : 'bg-white'}`}>
            <div className="flex items-center justify-between mb-6">
              <h3 className={`text-lg font-bold ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>{t.createUser}</h3>
              <button onClick={() => setShowModal(false)} className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800">
                <X size={18} />
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">{t.username}</label>
                <input 
                  type="text" 
                  value={newUserForm.username}
                  onChange={(e) => setNewUserForm({...newUserForm, username: e.target.value})}
                  className={`w-full mt-1 px-4 py-2.5 rounded-xl border text-sm ${
                    isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'
                  }`}
                />
              </div>
              <div>
                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">{t.email}</label>
                <input 
                  type="email" 
                  value={newUserForm.email}
                  onChange={(e) => setNewUserForm({...newUserForm, email: e.target.value})}
                  className={`w-full mt-1 px-4 py-2.5 rounded-xl border text-sm ${
                    isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'
                  }`}
                />
              </div>
              <div>
                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">{t.password}</label>
                <input 
                  type="password" 
                  value={newUserForm.password}
                  onChange={(e) => setNewUserForm({...newUserForm, password: e.target.value})}
                  className={`w-full mt-1 px-4 py-2.5 rounded-xl border text-sm ${
                    isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'
                  }`}
                />
              </div>
              <div>
                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">{t.phone}</label>
                <input 
                  type="text" 
                  value={newUserForm.phone}
                  onChange={(e) => setNewUserForm({...newUserForm, phone: e.target.value})}
                  className={`w-full mt-1 px-4 py-2.5 rounded-xl border text-sm ${
                    isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'
                  }`}
                />
              </div>
              <div>
                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">{t.dob}</label>
                <input 
                  type="date" 
                  value={newUserForm.dob}
                  onChange={(e) => setNewUserForm({...newUserForm, dob: e.target.value})}
                  className={`w-full mt-1 px-4 py-2.5 rounded-xl border text-sm ${
                    isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'
                  }`}
                />
              </div>
              <div>
                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">{t.gender}</label>
                <select 
                  value={newUserForm.gender}
                  onChange={(e) => setNewUserForm({...newUserForm, gender: e.target.value})}
                  className={`w-full mt-1 px-4 py-2.5 rounded-xl border text-sm ${
                    isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'
                  }`}
                >
                  <option value="Nam">{t.male}</option>
                  <option value="Nữ">{t.female}</option>
                </select>
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button 
                onClick={() => setShowModal(false)}
                className={`flex-1 py-2.5 rounded-xl font-semibold text-sm ${
                  isDarkMode ? 'bg-slate-800 hover:bg-slate-700' : 'bg-slate-100 hover:bg-slate-200'
                }`}
              >
                {t.cancel}
              </button>
              <button 
                onClick={handleCreateUser}
                className="flex-1 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm"
              >
                {t.save}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Edit User Modal */}
      {showEditModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className={`w-full max-w-md rounded-2xl p-6 ${isDarkMode ? 'bg-slate-900' : 'bg-white'}`}>
            <div className="flex items-center justify-between mb-6">
              <h3 className={`text-lg font-bold ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>{t.updateUser}</h3>
              <button onClick={() => setShowEditModal(false)} className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800">
                <X size={18} />
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">{t.username}</label>
                <input 
                  type="text" 
                  value={editForm.username}
                  onChange={(e) => setEditForm({...editForm, username: e.target.value})}
                  className={`w-full mt-1 px-4 py-2.5 rounded-xl border text-sm ${
                    isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'
                  }`}
                />
              </div>
              <div>
                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">{t.email}</label>
                <input 
                  type="email" 
                  value={editForm.email}
                  onChange={(e) => setEditForm({...editForm, email: e.target.value})}
                  className={`w-full mt-1 px-4 py-2.5 rounded-xl border text-sm ${
                    isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'
                  }`}
                />
              </div>
              <div>
                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">{t.phone}</label>
                <input 
                  type="text" 
                  value={editForm.phone}
                  onChange={(e) => setEditForm({...editForm, phone: e.target.value})}
                  className={`w-full mt-1 px-4 py-2.5 rounded-xl border text-sm ${
                    isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'
                  }`}
                />
              </div>
              <div>
                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">{t.dob}</label>
                <input 
                  type="date" 
                  value={editForm.dob}
                  onChange={(e) => setEditForm({...editForm, dob: e.target.value})}
                  className={`w-full mt-1 px-4 py-2.5 rounded-xl border text-sm ${
                    isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'
                  }`}
                />
              </div>
              <div>
                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">{t.gender}</label>
                <select 
                  value={editForm.gender}
                  onChange={(e) => setEditForm({...editForm, gender: e.target.value})}
                  className={`w-full mt-1 px-4 py-2.5 rounded-xl border text-sm ${
                    isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'
                  }`}
                >
                  <option value="Nam">{t.male}</option>
                  <option value="Nữ">{t.female}</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">{t.status}</label>
                <select 
                  value={editForm.status}
                  onChange={(e) => setEditForm({...editForm, status: e.target.value})}
                  className={`w-full mt-1 px-4 py-2.5 rounded-xl border text-sm ${
                    isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'
                  }`}
                >
                  <option value="ACTIVE">{t.active}</option>
                  <option value="INACTIVE">{t.inactive}</option>
                </select>
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button 
                onClick={() => setShowEditModal(false)}
                className={`flex-1 py-2.5 rounded-xl font-semibold text-sm ${
                  isDarkMode ? 'bg-slate-800 hover:bg-slate-700' : 'bg-slate-100 hover:bg-slate-200'
                }`}
              >
                {t.cancel}
              </button>
              <button 
                onClick={handleUpdateUser}
                className="flex-1 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm"
              >
                {t.save}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
