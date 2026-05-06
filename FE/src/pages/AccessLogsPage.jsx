import React, { useState, useEffect } from 'react'
import { useOutletContext } from 'react-router-dom'
import {
    Shield, UserPlus, Search, Filter, Calendar, Clock, Globe,
    Monitor, CheckCircle2, XCircle, AlertCircle, RefreshCw,
    User, Mail, Phone, Users, Loader2, Eye, EyeOff
} from 'lucide-react'
import UserCreateModalWithRoles from '../components/UserCreateModalWithRoles'

const API_BASE = import.meta.env.VITE_API_URL

const translations = {
    vi: {
        title: 'Nhật Ký Truy Cập',
        addUser: 'Tạo Người Dùng',
        searchPlaceholder: 'Tìm kiếm theo username, email, hành động...',
        username: 'Người Dùng',
        email: 'Email',
        action: 'Hành Động',
        ipAddress: 'Địa Chỉ IP',
        userAgent: 'Thiết Bị',
        time: 'Thời Gian',
        noData: 'Không có dữ liệu',
        refresh: 'Làm Mới',
        loading: 'Đang tải...',
        totalLogs: 'Tổng Nhật Ký',
        todayLogs: 'Hôm Nay',
        successActions: 'Thành Công',
        failedActions: 'Thất Bại',
        filterByAction: 'Lọc theo hành động',
        allActions: 'Tất cả',
        loginSuccess: 'Đăng nhập thành công',
        loginFailed: 'Đăng nhập thất bại',
        createUser: 'Tạo người dùng',
        updateUser: 'Cập nhật người dùng',
        deleteUser: 'Xóa người dùng',
        emailVerified: 'Xác thực email',
        results: 'kết quả'
    },
    en: {
        title: 'Access Logs',
        addUser: 'Create User',
        searchPlaceholder: 'Search by username, email, action...',
        username: 'Username',
        email: 'Email',
        action: 'Action',
        ipAddress: 'IP Address',
        userAgent: 'Device',
        time: 'Time',
        noData: 'No data',
        refresh: 'Refresh',
        loading: 'Loading...',
        totalLogs: 'Total Logs',
        todayLogs: 'Today',
        successActions: 'Success',
        failedActions: 'Failed',
        filterByAction: 'Filter by action',
        allActions: 'All',
        loginSuccess: 'Login Success',
        loginFailed: 'Login Failed',
        createUser: 'Create User',
        updateUser: 'Update User',
        deleteUser: 'Delete User',
        emailVerified: 'Email Verified',
        results: 'results'
    }
}

const actionColors = {
    'LOGIN_SUCCESS': 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20',
    'LOGIN_FAILED': 'bg-rose-500/10 text-rose-500 border-rose-500/20',
    'LOGIN_FAILED_WRONG_PASSWORD': 'bg-rose-500/10 text-rose-500 border-rose-500/20',
    'LOGIN_FAILED_EMAIL_NOT_VERIFIED': 'bg-amber-500/10 text-amber-500 border-amber-500/20',
    'LOGIN_FAILED_ACCOUNT_INACTIVE': 'bg-orange-500/10 text-orange-500 border-orange-500/20',
    'CREATE_USER': 'bg-blue-500/10 text-blue-500 border-blue-500/20',
    'UPDATE_USER': 'bg-purple-500/10 text-purple-500 border-purple-500/20',
    'DELETE_USER': 'bg-red-500/10 text-red-500 border-red-500/20',
    'EMAIL_VERIFIED': 'bg-green-500/10 text-green-500 border-green-500/20',
    'CHANGE_PASSWORD': 'bg-indigo-500/10 text-indigo-500 border-indigo-500/20'
}

const actionIcons = {
    'LOGIN_SUCCESS': CheckCircle2,
    'LOGIN_FAILED': XCircle,
    'LOGIN_FAILED_WRONG_PASSWORD': XCircle,
    'LOGIN_FAILED_EMAIL_NOT_VERIFIED': AlertCircle,
    'LOGIN_FAILED_ACCOUNT_INACTIVE': AlertCircle,
    'CREATE_USER': UserPlus,
    'UPDATE_USER': User,
    'DELETE_USER': XCircle,
    'EMAIL_VERIFIED': CheckCircle2,
    'CHANGE_PASSWORD': Shield
}

// Helper function for role badge colors
const getRoleBadgeColor = (role) => {
    const colors = {
        'SUPER_ADMIN': 'bg-red-500/10 text-red-500 border-red-500/20',
        'HR_MANAGER': 'bg-blue-500/10 text-blue-500 border-blue-500/20',
        'PAYROLL_ACCOUNTANT': 'bg-green-500/10 text-green-500 border-green-500/20',
        'EMPLOYEE': 'bg-slate-500/10 text-slate-500 border-slate-500/20'
    }
    return colors[role] || 'bg-slate-500/10 text-slate-500 border-slate-500/20'
}

export default function AccessLogsPage() {
    const { isDarkMode, language } = useOutletContext() || { isDarkMode: false, language: 'vi' }
    const lang = language || 'vi'
    const t = translations[lang]

    const [logs, setLogs] = useState([])
    const [users, setUsers] = useState([])
    const [loading, setLoading] = useState(false)
    const [usersLoading, setUsersLoading] = useState(false)
    const [searchTerm, setSearchTerm] = useState('')
    const [actionFilter, setActionFilter] = useState('all')
    const [showCreateModal, setShowCreateModal] = useState(false)
    const [activeTab, setActiveTab] = useState('logs')

    const fetchLogs = async () => {
        setLoading(true)
        try {
            const token = localStorage.getItem('access_token')
            const res = await fetch(`${API_BASE}/api/v1/admin/access-logs`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await res.json()
            setLogs(data.data || [])
        } catch (err) {
            console.error('Error fetching logs:', err)
        } finally {
            setLoading(false)
        }
    }

    const fetchUsers = async () => {
        setUsersLoading(true)
        try {
            const token = localStorage.getItem('access_token')
            const res = await fetch(`${API_BASE}/api/v1/admin/users-with-roles`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await res.json()
            setUsers(data.data || [])
        } catch (err) {
            console.error('Error fetching users:', err)
        } finally {
            setUsersLoading(false)
        }
    }

    useEffect(() => {
        fetchLogs()
        fetchUsers()
    }, [])

    const filteredLogs = logs.filter(log => {
        const matchesSearch =
            log.Username?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            log.Email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            log.Action?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            log.IPAddress?.toLowerCase().includes(searchTerm.toLowerCase())

        const matchesAction = actionFilter === 'all' || log.Action === actionFilter

        return matchesSearch && matchesAction
    })

    const filteredUsers = users.filter(user =>
        user.Username?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.Email?.toLowerCase().includes(searchTerm.toLowerCase())
    )

    const formatDateTime = (dateStr) => {
        if (!dateStr) return 'N/A'
        const date = new Date(dateStr)
        return date.toLocaleString(lang === 'vi' ? 'vi-VN' : 'en-US', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        })
    }

    const getActionLabel = (action) => {
        const labels = {
            'LOGIN_SUCCESS': 'Đăng nhập thành công',
            'LOGIN_FAILED': 'Đăng nhập thất bại',
            'LOGIN_FAILED_WRONG_PASSWORD': 'Sai mật khẩu',
            'LOGIN_FAILED_EMAIL_NOT_VERIFIED': 'Email chưa xác thực',
            'LOGIN_FAILED_ACCOUNT_INACTIVE': 'Tài khoản bị khóa',
            'CREATE_USER': 'Tạo người dùng',
            'UPDATE_USER': 'Cập nhật người dùng',
            'DELETE_USER': 'Xóa người dùng',
            'EMAIL_VERIFIED': 'Xác thực email',
            'CHANGE_PASSWORD': 'Đổi mật khẩu'
        }
        return labels[action] || action
    }

    // Stats
    const totalLogs = logs.length
    const todayLogs = logs.filter(log => {
        const logDate = new Date(log.AccessTime).toDateString()
        return logDate === new Date().toDateString()
    }).length
    const successActions = logs.filter(log =>
        log.Action?.includes('SUCCESS') || log.Action === 'EMAIL_VERIFIED' || log.Action === 'CREATE_USER'
    ).length
    const failedActions = logs.filter(log => log.Action?.includes('FAILED')).length

    const totalUsers = users.length
    const activeUsers = users.filter(u => u.Status === 'ACTIVE').length

    const uniqueActions = [...new Set(logs.map(log => log.Action))].filter(Boolean)

    const tabs = [
        { id: 'logs', label: 'Nhật Ký Truy Cập', icon: Shield },
        { id: 'users', label: 'Danh Sách Người Dùng', icon: Users }
    ]

    return (
        <div className={`p-6 flex flex-col gap-6 ${isDarkMode ? 'text-slate-300' : 'text-slate-800'}`}>

            {/* Header */}
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

                <div className="flex items-center gap-3">
                    <button
                        onClick={() => { fetchLogs(); fetchUsers(); }}
                        disabled={loading || usersLoading}
                        className="text-xs px-3 py-1.5 bg-blue-600/10 text-blue-600 rounded-lg flex items-center gap-2 hover:bg-blue-600/20 disabled:opacity-50"
                    >
                        <RefreshCw size={14} className={(loading || usersLoading) ? 'animate-spin' : ''} />
                        {t.refresh}
                    </button>
                    <button
                        onClick={() => setShowCreateModal(true)}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-semibold text-sm flex items-center gap-2 shadow-lg shadow-blue-600/20 transition-all"
                    >
                        <UserPlus size={16} /> {t.addUser}
                    </button>
                </div>
            </div>

            {/* Stats Cards */}
            {activeTab === 'logs' ? (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    <div className={`p-3 rounded-lg flex items-center justify-between border ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
                        }`}>
                        <div>
                            <p className="text-[9px] font-bold text-blue-500 uppercase tracking-wide">{t.totalLogs}</p>
                            <h3 className={`text-base font-black mt-0.5 ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                                {loading ? '...' : totalLogs}
                            </h3>
                        </div>
                        <div className="bg-blue-500/10 p-2 rounded-lg">
                            <Shield size={16} className="text-blue-500" />
                        </div>
                    </div>

                    <div className={`p-3 rounded-lg flex items-center justify-between border ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
                        }`}>
                        <div>
                            <p className="text-[9px] font-bold text-amber-500 uppercase tracking-wide">{t.todayLogs}</p>
                            <h3 className={`text-base font-black mt-0.5 ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                                {loading ? '...' : todayLogs}
                            </h3>
                        </div>
                        <div className="bg-amber-500/10 p-2 rounded-lg">
                            <Calendar size={16} className="text-amber-500" />
                        </div>
                    </div>

                    <div className={`p-3 rounded-lg flex items-center justify-between border ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
                        }`}>
                        <div>
                            <p className="text-[9px] font-bold text-emerald-500 uppercase tracking-wide">{t.successActions}</p>
                            <h3 className={`text-base font-black mt-0.5 ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                                {loading ? '...' : successActions}
                            </h3>
                        </div>
                        <div className="bg-emerald-500/10 p-2 rounded-lg">
                            <CheckCircle2 size={16} className="text-emerald-500" />
                        </div>
                    </div>

                    <div className={`p-3 rounded-lg flex items-center justify-between border ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
                        }`}>
                        <div>
                            <p className="text-[9px] font-bold text-rose-500 uppercase tracking-wide">{t.failedActions}</p>
                            <h3 className={`text-base font-black mt-0.5 ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                                {loading ? '...' : failedActions}
                            </h3>
                        </div>
                        <div className="bg-rose-500/10 p-2 rounded-lg">
                            <XCircle size={16} className="text-rose-500" />
                        </div>
                    </div>
                </div>
            ) : (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    <div className={`p-3 rounded-lg flex items-center justify-between border ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
                        }`}>
                        <div>
                            <p className="text-[9px] font-bold text-blue-500 uppercase tracking-wide">Tổng Người Dùng</p>
                            <h3 className={`text-base font-black mt-0.5 ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                                {usersLoading ? '...' : totalUsers}
                            </h3>
                        </div>
                        <div className="bg-blue-500/10 p-2 rounded-lg">
                            <Users size={16} className="text-blue-500" />
                        </div>
                    </div>

                    <div className={`p-3 rounded-lg flex items-center justify-between border ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
                        }`}>
                        <div>
                            <p className="text-[9px] font-bold text-emerald-500 uppercase tracking-wide">Đang Hoạt Động</p>
                            <h3 className={`text-base font-black mt-0.5 ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                                {usersLoading ? '...' : activeUsers}
                            </h3>
                        </div>
                        <div className="bg-emerald-500/10 p-2 rounded-lg">
                            <CheckCircle2 size={16} className="text-emerald-500" />
                        </div>
                    </div>

                    <div className={`p-3 rounded-lg flex items-center justify-between border ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
                        }`}>
                        <div>
                            <p className="text-[9px] font-bold text-amber-500 uppercase tracking-wide">Đăng Nhập Hôm Nay</p>
                            <h3 className={`text-base font-black mt-0.5 ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                                {loading ? '...' : todayLogs}
                            </h3>
                        </div>
                        <div className="bg-amber-500/10 p-2 rounded-lg">
                            <Calendar size={16} className="text-amber-500" />
                        </div>
                    </div>

                    <div className={`p-3 rounded-lg flex items-center justify-between border ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
                        }`}>
                        <div>
                            <p className="text-[9px] font-bold text-rose-500 uppercase tracking-wide">Đăng Nhập Thất Bại</p>
                            <h3 className={`text-base font-black mt-0.5 ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                                {loading ? '...' : failedActions}
                            </h3>
                        </div>
                        <div className="bg-rose-500/10 p-2 rounded-lg">
                            <XCircle size={16} className="text-rose-500" />
                        </div>
                    </div>
                </div>
            )}

            {/* Filter Bar */}
            <div className={`p-3 rounded-lg border ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
                }`}>
                <div className={`grid ${activeTab === 'logs' ? 'grid-cols-1 md:grid-cols-2' : 'grid-cols-1'} gap-3`}>
                    {/* Search */}
                    <div className="flex items-center gap-2">
                        <Search className="text-slate-400" size={16} />
                        <input
                            type="text"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="bg-transparent w-full focus:outline-none text-xs"
                            placeholder={activeTab === 'logs' ? t.searchPlaceholder : 'Tìm kiếm người dùng...'}
                        />
                    </div>

                    {/* Action Filter - Only show for logs tab */}
                    {activeTab === 'logs' && (
                        <div className="flex items-center gap-2">
                            <Filter className="text-slate-400" size={16} />
                            <select
                                value={actionFilter}
                                onChange={(e) => setActionFilter(e.target.value)}
                                className={`bg-transparent w-full focus:outline-none text-xs ${isDarkMode ? 'text-slate-300' : 'text-slate-800'
                                    }`}
                            >
                                <option value="all">{t.allActions}</option>
                                {uniqueActions.map(action => (
                                    <option key={action} value={action}>{getActionLabel(action)}</option>
                                ))}
                            </select>
                        </div>
                    )}
                </div>

                {((activeTab === 'logs' && filteredLogs.length > 0) || (activeTab === 'users' && filteredUsers.length > 0)) && (
                    <div className="mt-2 text-[10px] text-slate-400">
                        Hiển thị {activeTab === 'logs' ? filteredLogs.length : filteredUsers.length} {t.results}
                    </div>
                )}
            </div>

            {/* Logs Table */}
            {activeTab === 'logs' && (
                <div className={`border overflow-hidden rounded-lg ${isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200'
                    }`}>
                    <div className="overflow-x-auto">
                        <table className="w-full text-xs">
                            <thead className={isDarkMode ? 'bg-slate-800' : 'bg-slate-100'}>
                                <tr>
                                    <th className="p-6 text-left text-[10px] font-bold uppercase tracking-wider">{t.username}</th>
                                    <th className="p-3 text-left text-[10px] font-bold uppercase tracking-wider">{t.email}</th>
                                    <th className="p-3 text-left text-[10px] font-bold uppercase tracking-wider">Vai Trò</th>
                                    <th className="p-3 text-left text-[10px] font-bold uppercase tracking-wider">{t.action}</th>
                                    <th className="p-3 text-left text-[10px] font-bold uppercase tracking-wider">{t.ipAddress}</th>
                                    <th className="p-3 text-left text-[10px] font-bold uppercase tracking-wider">{t.userAgent}</th>
                                    <th className="p-3 text-left text-[10px] font-bold uppercase tracking-wider">{t.time}</th>
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
                                ) : filteredLogs.length === 0 ? (
                                    <tr>
                                        <td colSpan="7" className="text-center p-10 text-slate-400">{t.noData}</td>
                                    </tr>
                                ) : filteredLogs.map((log, idx) => {
                                    const ActionIcon = actionIcons[log.Action] || AlertCircle
                                    const actionColor = actionColors[log.Action] || 'bg-slate-500/10 text-slate-500 border-slate-500/20'

                                    return (
                                        <tr
                                            key={log.LogID || idx}
                                            className="transition-colors hover:bg-slate-500/5"
                                        >
                                            <td className="p-2.5">
                                                <div className="flex items-center gap-2">
                                                    <div className={`w-6 h-6 rounded-lg flex items-center justify-center font-bold  ${isDarkMode ? 'bg-slate-800 text-slate-400' : 'bg-slate-100 text-slate-600'
                                                        }`}>
                                                        {log.Username?.[0]?.toUpperCase() || 'U'}
                                                    </div>
                                                    <span className="font-medium text-sm">{log.Username || 'N/A'}</span>
                                                </div>
                                            </td>
                                            <td className="p-6 text-slate-500 text-xs">{log.Email || 'N/A'}</td>
                                            <td className="p-2.5">
                                                <div className="flex flex-wrap gap-1">
                                                    {log.UserRoles && log.UserRoles.length > 0 ? (
                                                        log.UserRoles.map((role, roleIdx) => (
                                                            <span key={roleIdx} className={`px-1.5 py-0.5 text-[9px] rounded border font-semibold ${getRoleBadgeColor(role)}`}>
                                                                {role}
                                                            </span>
                                                        ))
                                                    ) : (
                                                        <span className="text-slate-400 text-[10px]">-</span>
                                                    )}
                                                </div>
                                            </td>
                                            <td className="p-2.5">
                                                <span className={`px-2 py-1 rounded-lg text-[10px] font-semibold flex items-center gap-1.5 w-fit border ${actionColor}`}>
                                                    <ActionIcon size={12} />
                                                    {getActionLabel(log.Action)}
                                                </span>
                                            </td>
                                            <td className="p-2.5">
                                                <div className="flex items-center gap-1.5 text-slate-500 text-xs">
                                                    <Globe size={12} />
                                                    {log.IPAddress || 'N/A'}
                                                </div>
                                            </td>
                                            <td className="p-2.5">
                                                <div className="flex items-center gap-1.5 text-slate-500 max-w-[200px] truncate text-xs">
                                                    <Monitor size={12} className="flex-shrink-0" />
                                                    <span className="truncate" title={log.UserAgent}>
                                                        {log.UserAgent || 'N/A'}
                                                    </span>
                                                </div>
                                            </td>
                                            <td className="p-2.5">
                                                <div className="flex items-center gap-1.5 text-slate-500 text-xs">
                                                    <Clock size={12} />
                                                    {formatDateTime(log.AccessTime)}
                                                </div>
                                            </td>
                                        </tr>
                                    )
                                })}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}

            {/* Users Table */}
            {activeTab === 'users' && (
                <div className={`border overflow-hidden rounded-lg ${isDarkMode ? 'bg-slate-900/40 border-slate-800' : 'bg-white border-slate-200'
                    }`}>
                    <div className="overflow-x-auto">
                        <table className="w-full text-xs">
                            <thead className={isDarkMode ? 'bg-slate-800' : 'bg-slate-100'}>
                                <tr>
                                    <th className="p-4 text-left text-[10px] font-bold uppercase tracking-wider">Tên Đăng Nhập</th>
                                    <th className="p-4 text-left text-[10px] font-bold uppercase tracking-wider">Email</th>
                                    <th className="p-4 text-left text-[10px] font-bold uppercase tracking-wider">Vai Trò</th>
                                    <th className="p-4 text-left text-[10px] font-bold uppercase tracking-wider">Số Điện Thoại</th>
                                    <th className="p-4 text-left text-[10px] font-bold uppercase tracking-wider">Giới Tính</th>
                                    <th className="p-4 text-left text-[10px] font-bold uppercase tracking-wider">Trạng Thái</th>
                                    <th className="p-4 text-left text-[10px] font-bold uppercase tracking-wider">Ngày Tạo</th>
                                </tr>
                            </thead>
                            <tbody className={`divide-y ${isDarkMode ? 'divide-slate-800' : 'divide-slate-100'}`}>
                                {usersLoading ? (
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
                                        className="transition-colors hover:bg-slate-500/5"
                                    >
                                        <td className="p-4">
                                            <div className="flex items-center gap-3">
                                                <div className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold text-xs ${isDarkMode ? 'bg-blue-900 text-blue-400' : 'bg-blue-100 text-blue-600'
                                                    }`}>
                                                    {user.Username?.[0]?.toUpperCase() || 'U'}
                                                </div>
                                                <span className="font-semibold text-sm">{user.Username}</span>
                                            </div>
                                        </td>
                                        <td className="p-4 text-slate-500">{user.Email}</td>
                                        <td className="p-4">
                                            <div className="flex flex-wrap gap-1">
                                                {user.Roles && user.Roles.length > 0 ? (
                                                    user.Roles.map((role, idx) => (
                                                        <span key={idx} className={`px-2 py-0.5 text-[10px] rounded-lg border font-semibold ${getRoleBadgeColor(role)}`}>
                                                            {role}
                                                        </span>
                                                    ))
                                                ) : (
                                                    <span className="text-slate-400 text-[10px]">No roles</span>
                                                )}
                                            </div>
                                        </td>
                                        <td className="p-4 text-slate-500">{user.PhoneNumber || 'N/A'}</td>
                                        <td className="p-4 text-slate-500">{user.Gender || 'N/A'}</td>
                                        <td className="p-4">
                                            <span className={`px-2.5 py-1 rounded-lg text-[10px] font-semibold ${user.Status === 'ACTIVE'
                                                ? 'bg-emerald-100 text-emerald-600 dark:bg-emerald-500/10 dark:text-emerald-500'
                                                : 'bg-rose-100 text-rose-600 dark:bg-rose-500/10 dark:text-rose-500'
                                                }`}>
                                                {user.Status === 'ACTIVE' ? 'Hoạt Động' : 'Đã Khóa'}
                                            </span>
                                        </td>
                                        <td className="p-4 text-slate-500">{formatDateTime(user.CreatedAt)}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}

            {/* Create User Modal */}
            <UserCreateModalWithRoles
                isOpen={showCreateModal}
                onClose={() => setShowCreateModal(false)}
                isDarkMode={isDarkMode}
                onSuccess={(data) => {
                    console.log('User created successfully:', data)
                    fetchLogs() // Refresh logs to show CREATE_USER action
                }}
            />
        </div>
    )
}
