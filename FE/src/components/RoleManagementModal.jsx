import React, { useState, useEffect } from 'react'
import { X, Shield, Check, Loader2 } from 'lucide-react'

const API_BASE = import.meta.env.VITE_API_URL

export default function RoleManagementModal({ isOpen, onClose, user, isDarkMode, onSuccess }) {
    const [roles, setRoles] = useState([])
    const [userRoles, setUserRoles] = useState([])
    const [loading, setLoading] = useState(false)
    const [saving, setSaving] = useState(false)
    const [selectedRoles, setSelectedRoles] = useState([])

    useEffect(() => {
        if (isOpen && user) {
            fetchRoles()
            fetchUserRoles()
        }
    }, [isOpen, user])

    const fetchRoles = async () => {
        try {
            const res = await fetch(`${API_BASE}/api/v1/auth/roles`)
            const data = await res.json()
            if (data.status === 'success') {
                setRoles(data.data || [])
            }
        } catch (err) {
            console.error('Error fetching roles:', err)
        }
    }

    const fetchUserRoles = async () => {
        setLoading(true)
        try {
            const res = await fetch(`${API_BASE}/api/v1/auth/users/${user.UserID}/roles`)
            const data = await res.json()
            if (data.status === 'success') {
                const roleIds = data.data.map(r => r.RoleID)
                setUserRoles(roleIds)
                setSelectedRoles(roleIds)
            }
        } catch (err) {
            console.error('Error fetching user roles:', err)
        } finally {
            setLoading(false)
        }
    }

    const handleToggleRole = (roleId) => {
        setSelectedRoles(prev => {
            if (prev.includes(roleId)) {
                return prev.filter(id => id !== roleId)
            } else {
                return [...prev, roleId]
            }
        })
    }

    const handleSave = async () => {
        setSaving(true)
        try {
            const res = await fetch(`${API_BASE}/api/v1/auth/users/${user.UserID}/roles`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ roles: selectedRoles })
            })
            const data = await res.json()

            if (data.status === 'success') {
                if (onSuccess) onSuccess()
                onClose()
            } else {
                alert(data.message || 'Lỗi cập nhật vai trò')
            }
        } catch (err) {
            alert('Không thể cập nhật vai trò')
        } finally {
            setSaving(false)
        }
    }

    const getRoleBadgeColor = (roleName) => {
        const colors = {
            'SUPER_ADMIN': 'bg-red-500/10 text-red-400 border-red-500/20',
            'HR_MANAGER': 'bg-blue-500/10 text-blue-400 border-blue-500/20',
            'PAYROLL_ACCOUNTANT': 'bg-green-500/10 text-green-400 border-green-500/20',
            'EMPLOYEE': 'bg-gray-500/10 text-gray-400 border-gray-500/20'
        }
        return colors[roleName] || 'bg-slate-500/10 text-slate-400 border-slate-500/20'
    }

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
            <div className={`w-full max-w-2xl rounded-2xl p-6 ${isDarkMode ? 'bg-slate-900' : 'bg-white'}`}>
                {/* Header */}
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h3 className={`text-lg font-bold ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                            Quản Lý Vai Trò
                        </h3>
                        <p className="text-sm text-slate-400 mt-1">
                            Người dùng: <span className="text-blue-400 font-medium">{user?.Username}</span>
                        </p>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
                    >
                        <X size={18} />
                    </button>
                </div>

                {/* Content */}
                {loading ? (
                    <div className="text-center py-12">
                        <Loader2 className="animate-spin text-blue-500 mx-auto mb-4" size={32} />
                        <p className="text-slate-400">Đang tải...</p>
                    </div>
                ) : (
                    <div className="space-y-3 max-h-[400px] overflow-y-auto">
                        {roles.map((role) => {
                            const isSelected = selectedRoles.includes(role.RoleID)

                            return (
                                <div
                                    key={role.RoleID}
                                    onClick={() => handleToggleRole(role.RoleID)}
                                    className={`p-4 rounded-xl border-2 transition-all cursor-pointer ${isSelected
                                            ? 'border-blue-500 bg-blue-500/5'
                                            : isDarkMode
                                                ? 'border-slate-700 hover:border-slate-600 bg-slate-800/50'
                                                : 'border-slate-200 hover:border-slate-300 bg-white'
                                        }`}
                                >
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center gap-3">
                                            <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${isSelected ? 'bg-blue-500' : isDarkMode ? 'bg-slate-700' : 'bg-slate-100'
                                                }`}>
                                                <Shield size={20} className={isSelected ? 'text-white' : 'text-slate-400'} />
                                            </div>
                                            <div>
                                                <h4 className={`font-semibold ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                                                    {role.RoleName}
                                                </h4>
                                                <p className="text-xs text-slate-400 mt-0.5">
                                                    {role.RoleName === 'SUPER_ADMIN' && 'Quản trị viên hệ thống'}
                                                    {role.RoleName === 'HR_MANAGER' && 'Quản lý nhân sự'}
                                                    {role.RoleName === 'PAYROLL_ACCOUNTANT' && 'Kế toán lương'}
                                                    {role.RoleName === 'EMPLOYEE' && 'Nhân viên'}
                                                </p>
                                            </div>
                                        </div>
                                        <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${isSelected
                                                ? 'bg-blue-500 border-blue-500'
                                                : isDarkMode ? 'border-slate-600' : 'border-slate-300'
                                            }`}>
                                            {isSelected && <Check size={14} className="text-white" />}
                                        </div>
                                    </div>
                                </div>
                            )
                        })}
                    </div>
                )}

                {/* Footer */}
                <div className="flex items-center justify-between mt-6 pt-6 border-t border-slate-700">
                    <div className="text-sm text-slate-400">
                        Đã chọn: <span className="text-white font-medium">{selectedRoles.length}</span> vai trò
                    </div>
                    <div className="flex gap-3">
                        <button
                            onClick={onClose}
                            className={`px-6 py-2.5 rounded-xl font-semibold text-sm ${isDarkMode ? 'bg-slate-800 hover:bg-slate-700' : 'bg-slate-100 hover:bg-slate-200'
                                }`}
                        >
                            Hủy
                        </button>
                        <button
                            onClick={handleSave}
                            disabled={saving}
                            className="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm flex items-center gap-2 disabled:opacity-50"
                        >
                            {saving ? (
                                <>
                                    <Loader2 size={16} className="animate-spin" />
                                    Đang lưu...
                                </>
                            ) : (
                                'Lưu thay đổi'
                            )}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}
