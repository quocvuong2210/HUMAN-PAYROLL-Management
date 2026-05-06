import React, { useState, useEffect } from 'react'
import { X, User, Mail, Lock, Phone, Calendar, Users, Loader2 } from 'lucide-react'

const API_BASE = import.meta.env.VITE_API_URL

export default function UserCreateModalWithRoles({ isOpen, onClose, isDarkMode, onSuccess }) {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        phoneNumber: '',
        dateOfBirth: '',
        gender: 'Nam',
        roleIds: []
    })

    const [roles, setRoles] = useState([])
    const [loading, setLoading] = useState(false)
    const [errors, setErrors] = useState({})
    const [rolesLoading, setRolesLoading] = useState(false)

    // Load roles khi modal mở
    useEffect(() => {
        if (isOpen) {
            fetchRoles()
        }
    }, [isOpen])

    const fetchRoles = async () => {
        setRolesLoading(true)
        try {
            // Lấy token từ localStorage
            const token = localStorage.getItem('access_token') || localStorage.getItem('accessToken') || localStorage.getItem('token')

            console.log('🔑 Token:', token ? 'Found' : 'Not found')
            console.log('🌐 API URL:', `${API_BASE}/api/v1/auth/roles`)

            const res = await fetch(`${API_BASE}/api/v1/auth/roles`, {
                headers: {
                    'Authorization': `Bearer ${token}` // Thêm token vào header
                }
            })
            const data = await res.json()

            console.log('📦 Roles response:', data)

            if (data.status === 'success') {
                setRoles(data.data || [])
                console.log('✅ Roles loaded:', data.data?.length || 0)
            } else {
                console.error('❌ Failed to load roles:', data.message)
            }
        } catch (err) {
            console.error('❌ Error fetching roles:', err)
        } finally {
            setRolesLoading(false)
        }
    }

    const handleChange = (e) => {
        const { name, value } = e.target
        setFormData(prev => ({
            ...prev,
            [name]: value
        }))
        // Clear error khi user nhập
        if (errors[name]) {
            setErrors(prev => ({ ...prev, [name]: '' }))
        }
    }

    const handleRoleToggle = (roleId) => {
        setFormData(prev => ({
            ...prev,
            roleIds: prev.roleIds.includes(roleId)
                ? prev.roleIds.filter(id => id !== roleId)
                : [...prev.roleIds, roleId]
        }))
        if (errors.roleIds) {
            setErrors(prev => ({ ...prev, roleIds: '' }))
        }
    }

    const validate = () => {
        const newErrors = {}

        // Username
        if (!formData.username.trim()) {
            newErrors.username = 'Tên đăng nhập là bắt buộc'
        } else if (formData.username.length < 3) {
            newErrors.username = 'Tên đăng nhập phải có ít nhất 3 ký tự'
        }

        // Email
        if (!formData.email.trim()) {
            newErrors.email = 'Email là bắt buộc'
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
            newErrors.email = 'Email không hợp lệ'
        }

        // Password
        if (!formData.password) {
            newErrors.password = 'Mật khẩu là bắt buộc'
        } else if (formData.password.length < 6) {
            newErrors.password = 'Mật khẩu phải có ít nhất 6 ký tự'
        }

        // Roles (optional - nếu không chọn sẽ default là EMPLOYEE)
        // if (formData.roleIds.length === 0) {
        //   newErrors.roleIds = 'Vui lòng chọn ít nhất một vai trò'
        // }

        setErrors(newErrors)
        return Object.keys(newErrors).length === 0
    }

    const handleSubmit = async (e) => {
        e.preventDefault()

        if (!validate()) {
            return
        }

        setLoading(true)

        try {
            const payload = {
                username: formData.username,
                email: formData.email,
                password: formData.password,
                phoneNumber: formData.phoneNumber || null,
                dateOfBirth: formData.dateOfBirth || null,
                gender: formData.gender,
                roleIds: formData.roleIds.length > 0 ? formData.roleIds : null // Nếu không chọn, backend sẽ set default
            }

            // Lấy token từ localStorage
            const token = localStorage.getItem('access_token') || localStorage.getItem('accessToken') || localStorage.getItem('token')

            const res = await fetch(`${API_BASE}/api/v1/auth/users`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}` // Thêm token vào header
                },
                body: JSON.stringify(payload)
            })

            const data = await res.json()

            if (data.status === 'success') {
                // Reset form
                setFormData({
                    username: '',
                    email: '',
                    password: '',
                    phoneNumber: '',
                    dateOfBirth: '',
                    gender: 'Nam',
                    roleIds: []
                })
                setErrors({})

                // Callback success
                if (onSuccess) {
                    onSuccess(data)
                }

                onClose()
            } else {
                setErrors({ submit: data.message || 'Có lỗi xảy ra' })
            }
        } catch (err) {
            console.error('Error creating user:', err)
            setErrors({ submit: 'Không thể kết nối đến server' })
        } finally {
            setLoading(false)
        }
    }

    const handleCancel = () => {
        setFormData({
            username: '',
            email: '',
            password: '',
            phoneNumber: '',
            dateOfBirth: '',
            gender: 'Nam',
            roleIds: []
        })
        setErrors({})
        onClose()
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

    const getRoleDescription = (roleName) => {
        const descriptions = {
            'SUPER_ADMIN': 'Quản trị viên hệ thống - Toàn quyền',
            'HR_MANAGER': 'Quản lý nhân sự - Quản lý nhân viên, chấm công',
            'PAYROLL_ACCOUNTANT': 'Kế toán lương - Tính lương, báo cáo',
            'EMPLOYEE': 'Nhân viên - Xem thông tin cá nhân'
        }
        return descriptions[roleName] || 'Vai trò hệ thống'
    }

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
            <div className={`w-full max-w-2xl rounded-2xl shadow-2xl max-h-[90vh] overflow-y-auto ${isDarkMode ? 'bg-slate-900' : 'bg-white'
                }`}>
                {/* Header */}
                <div className={`sticky top-0 z-10 flex items-center justify-between p-6 border-b ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
                    }`}>
                    <h2 className={`text-xl font-bold ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                        Tạo Người Dùng
                    </h2>
                    <button
                        onClick={handleCancel}
                        className={`p-2 rounded-lg transition-colors ${isDarkMode ? 'hover:bg-slate-800' : 'hover:bg-slate-100'
                            }`}
                    >
                        <X size={20} className="text-slate-400" />
                    </button>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="p-6 space-y-5">
                    {/* Error message */}
                    {errors.submit && (
                        <div className="bg-red-500/10 border border-red-500 text-red-500 px-4 py-3 rounded-xl text-sm">
                            {errors.submit}
                        </div>
                    )}

                    {/* Username */}
                    <div>
                        <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                            Tên đăng nhập <span className="text-red-500">*</span>
                        </label>
                        <div className="relative">
                            <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={18} />
                            <input
                                type="text"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                                className={`w-full pl-10 pr-4 py-2.5 rounded-xl border text-sm transition-colors ${errors.username
                                    ? 'border-red-500 focus:ring-red-500'
                                    : isDarkMode
                                        ? 'bg-slate-800 border-slate-700 focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
                                        : 'bg-white border-slate-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
                                    } ${isDarkMode ? 'text-white' : 'text-slate-800'}`}
                                placeholder="Nhập tên đăng nhập"
                            />
                        </div>
                        {errors.username && (
                            <p className="mt-1 text-xs text-red-500">{errors.username}</p>
                        )}
                    </div>

                    {/* Email */}
                    <div>
                        <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                            Email <span className="text-red-500">*</span>
                        </label>
                        <div className="relative">
                            <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={18} />
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                className={`w-full pl-10 pr-4 py-2.5 rounded-xl border text-sm transition-colors ${errors.email
                                    ? 'border-red-500 focus:ring-red-500'
                                    : isDarkMode
                                        ? 'bg-slate-800 border-slate-700 focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
                                        : 'bg-white border-slate-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
                                    } ${isDarkMode ? 'text-white' : 'text-slate-800'}`}
                                placeholder="example@email.com"
                            />
                        </div>
                        {errors.email && (
                            <p className="mt-1 text-xs text-red-500">{errors.email}</p>
                        )}
                    </div>

                    {/* Password */}
                    <div>
                        <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                            Mật khẩu <span className="text-red-500">*</span>
                        </label>
                        <div className="relative">
                            <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={18} />
                            <input
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                className={`w-full pl-10 pr-4 py-2.5 rounded-xl border text-sm transition-colors ${errors.password
                                    ? 'border-red-500 focus:ring-red-500'
                                    : isDarkMode
                                        ? 'bg-slate-800 border-slate-700 focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
                                        : 'bg-white border-slate-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
                                    } ${isDarkMode ? 'text-white' : 'text-slate-800'}`}
                                placeholder="••••••••"
                            />
                        </div>
                        {errors.password && (
                            <p className="mt-1 text-xs text-red-500">{errors.password}</p>
                        )}
                        <p className="mt-1 text-xs text-slate-400">Tối thiểu 6 ký tự</p>
                    </div>

                    {/* Phone & DOB */}
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                                Số điện thoại
                            </label>
                            <div className="relative">
                                <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={18} />
                                <input
                                    type="tel"
                                    name="phoneNumber"
                                    value={formData.phoneNumber}
                                    onChange={handleChange}
                                    className={`w-full pl-10 pr-4 py-2.5 rounded-xl border text-sm ${isDarkMode
                                        ? 'bg-slate-800 border-slate-700 focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
                                        : 'bg-white border-slate-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
                                        } ${isDarkMode ? 'text-white' : 'text-slate-800'}`}
                                    placeholder="0123456789"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                                Ngày sinh
                            </label>
                            <div className="relative">
                                <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={18} />
                                <input
                                    type="date"
                                    name="dateOfBirth"
                                    value={formData.dateOfBirth}
                                    onChange={handleChange}
                                    className={`w-full pl-10 pr-4 py-2.5 rounded-xl border text-sm ${isDarkMode
                                        ? 'bg-slate-800 border-slate-700 focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
                                        : 'bg-white border-slate-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
                                        } ${isDarkMode ? 'text-white' : 'text-slate-800'}`}
                                />
                            </div>
                        </div>
                    </div>

                    {/* Gender */}
                    <div>
                        <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                            Giới tính
                        </label>
                        <select
                            name="gender"
                            value={formData.gender}
                            onChange={handleChange}
                            className={`w-full px-4 py-2.5 rounded-xl border text-sm ${isDarkMode
                                ? 'bg-slate-800 border-slate-700 focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
                                : 'bg-white border-slate-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
                                } ${isDarkMode ? 'text-white' : 'text-slate-800'}`}
                        >
                            <option value="Nam">Nam</option>
                            <option value="Nữ">Nữ</option>
                        </select>
                    </div>

                    {/* Roles (Multi-select) */}
                    <div>
                        <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                            Vai trò {formData.roleIds.length === 0 && <span className="text-xs font-normal text-slate-400">(Mặc định: EMPLOYEE)</span>}
                        </label>

                        {rolesLoading ? (
                            <div className="text-center py-8">
                                <Loader2 className="animate-spin text-blue-500 mx-auto mb-2" size={24} />
                                <p className="text-sm text-slate-400">Đang tải vai trò...</p>
                            </div>
                        ) : (
                            <div className="space-y-2 max-h-[200px] overflow-y-auto">
                                {roles.map((role) => {
                                    const isSelected = formData.roleIds.includes(role.RoleID)

                                    return (
                                        <div
                                            key={role.RoleID}
                                            onClick={() => handleRoleToggle(role.RoleID)}
                                            className={`p-3 rounded-xl border-2 transition-all cursor-pointer ${isSelected
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
                                                        <Users size={18} className={isSelected ? 'text-white' : 'text-slate-400'} />
                                                    </div>
                                                    <div>
                                                        <h4 className={`font-semibold text-sm ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>
                                                            {role.RoleName}
                                                        </h4>
                                                        <p className="text-xs text-slate-400 mt-0.5">
                                                            {getRoleDescription(role.RoleName)}
                                                        </p>
                                                    </div>
                                                </div>
                                                <div className={`w-5 h-5 rounded border-2 flex items-center justify-center ${isSelected
                                                    ? 'bg-blue-500 border-blue-500'
                                                    : isDarkMode ? 'border-slate-600' : 'border-slate-300'
                                                    }`}>
                                                    {isSelected && (
                                                        <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                                                        </svg>
                                                    )}
                                                </div>
                                            </div>
                                        </div>
                                    )
                                })}
                            </div>
                        )}

                        {errors.roleIds && (
                            <p className="mt-1 text-xs text-red-500">{errors.roleIds}</p>
                        )}

                        {formData.roleIds.length > 0 && (
                            <div className="mt-2 flex flex-wrap gap-2">
                                {formData.roleIds.map(roleId => {
                                    const role = roles.find(r => r.RoleID === roleId)
                                    if (!role) return null
                                    return (
                                        <span
                                            key={roleId}
                                            className={`px-2 py-1 text-xs rounded-lg border ${getRoleBadgeColor(role.RoleName)}`}
                                        >
                                            {role.RoleName}
                                        </span>
                                    )
                                })}
                            </div>
                        )}
                    </div>

                    {/* Actions */}
                    <div className="flex gap-3 pt-4">
                        <button
                            type="button"
                            onClick={handleCancel}
                            className={`flex-1 py-2.5 rounded-xl font-semibold text-sm transition-colors ${isDarkMode
                                ? 'bg-slate-800 hover:bg-slate-700 text-white'
                                : 'bg-slate-100 hover:bg-slate-200 text-slate-800'
                                }`}
                        >
                            Hủy
                        </button>
                        <button
                            type="submit"
                            disabled={loading}
                            className="flex-1 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            {loading ? (
                                <>
                                    <Loader2 size={16} className="animate-spin" />
                                    Đang tạo...
                                </>
                            ) : (
                                'Tạo người dùng'
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}
