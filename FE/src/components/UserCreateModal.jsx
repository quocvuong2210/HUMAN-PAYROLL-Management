import React, { useState, useEffect } from 'react';
import Select from 'react-select';
import { X, User, Mail, Lock, Phone, Calendar, Users } from 'lucide-react';

const UserCreateModal = ({ isOpen, onClose, onSuccess }) => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        phoneNumber: '',
        dateOfBirth: '',
        gender: 'Male',
        roles: []
    });

    const [roles, setRoles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});

    // Load roles từ API
    useEffect(() => {
        if (isOpen) {
            fetchRoles();
        }
    }, [isOpen]);

    const fetchRoles = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/v2/auth/admin/roles', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });
            const data = await response.json();

            if (data.status === 'success') {
                // Format cho react-select
                const formattedRoles = data.data.map(role => ({
                    value: role.RoleID,
                    label: role.RoleName,
                    description: role.Description
                }));
                setRoles(formattedRoles);
            }
        } catch (error) {
            console.error('Error fetching roles:', error);
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
        // Clear error khi user nhập
        if (errors[name]) {
            setErrors(prev => ({ ...prev, [name]: '' }));
        }
    };

    const handleRoleChange = (selectedOptions) => {
        setFormData(prev => ({
            ...prev,
            roles: selectedOptions || []
        }));
        if (errors.roles) {
            setErrors(prev => ({ ...prev, roles: '' }));
        }
    };

    const validate = () => {
        const newErrors = {};

        if (!formData.username.trim()) {
            newErrors.username = 'Tên đăng nhập là bắt buộc';
        }

        if (!formData.email.trim()) {
            newErrors.email = 'Email là bắt buộc';
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
            newErrors.email = 'Email không hợp lệ';
        }

        if (!formData.password) {
            newErrors.password = 'Mật khẩu là bắt buộc';
        } else if (formData.password.length < 6) {
            newErrors.password = 'Mật khẩu phải có ít nhất 6 ký tự';
        }

        if (formData.roles.length === 0) {
            newErrors.roles = 'Vui lòng chọn ít nhất một vai trò';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!validate()) {
            return;
        }

        setLoading(true);

        try {
            // Prepare data
            const submitData = {
                username: formData.username,
                email: formData.email,
                password: formData.password,
                phone: formData.phoneNumber,
                dob: formData.dateOfBirth,
                gender: formData.gender,
                roles: formData.roles.map(role => role.value) // Chỉ gửi RoleID
            };

            const response = await fetch('http://localhost:5000/api/v2/users/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: JSON.stringify(submitData)
            });

            const data = await response.json();

            if (data.status === 'success') {
                // Reset form
                setFormData({
                    username: '',
                    email: '',
                    password: '',
                    phoneNumber: '',
                    dateOfBirth: '',
                    gender: 'Male',
                    roles: []
                });
                setErrors({});

                // Callback success
                if (onSuccess) {
                    onSuccess(data);
                }

                onClose();
            } else {
                setErrors({ submit: data.message || 'Có lỗi xảy ra' });
            }
        } catch (error) {
            console.error('Error creating user:', error);
            setErrors({ submit: 'Không thể kết nối đến server' });
        } finally {
            setLoading(false);
        }
    };

    const handleCancel = () => {
        setFormData({
            username: '',
            email: '',
            password: '',
            phoneNumber: '',
            dateOfBirth: '',
            gender: 'Male',
            roles: []
        });
        setErrors({});
        onClose();
    };

    if (!isOpen) return null;

    // Custom styles cho react-select (dark mode)
    const selectStyles = {
        control: (base, state) => ({
            ...base,
            backgroundColor: '#1e293b',
            borderColor: state.isFocused ? '#3b82f6' : '#334155',
            boxShadow: state.isFocused ? '0 0 0 1px #3b82f6' : 'none',
            '&:hover': {
                borderColor: '#3b82f6'
            }
        }),
        menu: (base) => ({
            ...base,
            backgroundColor: '#1e293b',
            border: '1px solid #334155'
        }),
        option: (base, state) => ({
            ...base,
            backgroundColor: state.isFocused ? '#334155' : '#1e293b',
            color: '#e2e8f0',
            '&:hover': {
                backgroundColor: '#334155'
            }
        }),
        multiValue: (base) => ({
            ...base,
            backgroundColor: '#3b82f6'
        }),
        multiValueLabel: (base) => ({
            ...base,
            color: '#ffffff'
        }),
        multiValueRemove: (base) => ({
            ...base,
            color: '#ffffff',
            '&:hover': {
                backgroundColor: '#2563eb',
                color: '#ffffff'
            }
        }),
        input: (base) => ({
            ...base,
            color: '#e2e8f0'
        }),
        placeholder: (base) => ({
            ...base,
            color: '#64748b'
        }),
        singleValue: (base) => ({
            ...base,
            color: '#e2e8f0'
        })
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm">
            <div className="bg-slate-800 rounded-lg shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
                {/* Header */}
                <div className="flex items-center justify-between p-6 border-b border-slate-700">
                    <h2 className="text-2xl font-bold text-white">Tạo Người Dùng</h2>
                    <button
                        onClick={handleCancel}
                        className="text-slate-400 hover:text-white transition-colors"
                    >
                        <X size={24} />
                    </button>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="p-6 space-y-4">
                    {/* Error message */}
                    {errors.submit && (
                        <div className="bg-red-500/10 border border-red-500 text-red-500 px-4 py-3 rounded-lg">
                            {errors.submit}
                        </div>
                    )}

                    {/* Username */}
                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">
                            Tên đăng nhập <span className="text-red-500">*</span>
                        </label>
                        <div className="relative">
                            <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={20} />
                            <input
                                type="text"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                                className={`w-full pl-10 pr-4 py-2.5 bg-slate-700 border ${errors.username ? 'border-red-500' : 'border-slate-600'
                                    } rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                                placeholder="Nhập tên đăng nhập"
                            />
                        </div>
                        {errors.username && (
                            <p className="mt-1 text-sm text-red-500">{errors.username}</p>
                        )}
                    </div>

                    {/* Email */}
                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">
                            Email <span className="text-red-500">*</span>
                        </label>
                        <div className="relative">
                            <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={20} />
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                className={`w-full pl-10 pr-4 py-2.5 bg-slate-700 border ${errors.email ? 'border-red-500' : 'border-slate-600'
                                    } rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                                placeholder="example@email.com"
                            />
                        </div>
                        {errors.email && (
                            <p className="mt-1 text-sm text-red-500">{errors.email}</p>
                        )}
                    </div>

                    {/* Password */}
                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">
                            Mật khẩu <span className="text-red-500">*</span>
                        </label>
                        <div className="relative">
                            <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={20} />
                            <input
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                className={`w-full pl-10 pr-4 py-2.5 bg-slate-700 border ${errors.password ? 'border-red-500' : 'border-slate-600'
                                    } rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                                placeholder="••••••••"
                            />
                        </div>
                        {errors.password && (
                            <p className="mt-1 text-sm text-red-500">{errors.password}</p>
                        )}
                    </div>

                    {/* Phone Number */}
                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">
                            Số điện thoại
                        </label>
                        <div className="relative">
                            <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={20} />
                            <input
                                type="tel"
                                name="phoneNumber"
                                value={formData.phoneNumber}
                                onChange={handleChange}
                                className="w-full pl-10 pr-4 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="0123456789"
                            />
                        </div>
                    </div>

                    {/* Date of Birth & Gender */}
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-2">
                                Ngày sinh
                            </label>
                            <div className="relative">
                                <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={20} />
                                <input
                                    type="date"
                                    name="dateOfBirth"
                                    value={formData.dateOfBirth}
                                    onChange={handleChange}
                                    className="w-full pl-10 pr-4 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-2">
                                Giới tính
                            </label>
                            <select
                                name="gender"
                                value={formData.gender}
                                onChange={handleChange}
                                className="w-full px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            >
                                <option value="Male">Nam</option>
                                <option value="Female">Nữ</option>
                                <option value="Other">Khác</option>
                            </select>
                        </div>
                    </div>

                    {/* Roles (Multi-select) */}
                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">
                            Vai trò <span className="text-red-500">*</span>
                        </label>
                        <Select
                            isMulti
                            name="roles"
                            options={roles}
                            value={formData.roles}
                            onChange={handleRoleChange}
                            styles={selectStyles}
                            placeholder="Chọn vai trò..."
                            noOptionsMessage={() => "Không có vai trò"}
                            className="react-select-container"
                            classNamePrefix="react-select"
                            formatOptionLabel={(option) => (
                                <div>
                                    <div className="font-medium">{option.label}</div>
                                    {option.description && (
                                        <div className="text-xs text-slate-400">{option.description}</div>
                                    )}
                                </div>
                            )}
                        />
                        {errors.roles && (
                            <p className="mt-1 text-sm text-red-500">{errors.roles}</p>
                        )}
                    </div>

                    {/* Actions */}
                    <div className="flex justify-end gap-3 pt-4">
                        <button
                            type="button"
                            onClick={handleCancel}
                            className="px-6 py-2.5 bg-slate-700 text-white rounded-lg hover:bg-slate-600 transition-colors"
                        >
                            Hủy
                        </button>
                        <button
                            type="submit"
                            disabled={loading}
                            className="px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                        >
                            {loading ? (
                                <>
                                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
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
    );
};

export default UserCreateModal;
