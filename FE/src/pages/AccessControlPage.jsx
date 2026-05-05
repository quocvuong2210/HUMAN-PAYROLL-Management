import React, { useState, useEffect } from 'react';
import { Shield, Users, Key, Settings, ChevronRight, Edit, Plus, X, Check } from 'lucide-react';

const AccessControlPage = () => {
    const [roles, setRoles] = useState([]);
    const [permissions, setPermissions] = useState([]);
    const [functions, setFunctions] = useState([]);
    const [selectedRole, setSelectedRole] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);

    // Temporary state for editing
    const [tempPermissions, setTempPermissions] = useState([]);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem('access_token');
            const headers = {
                'Authorization': `Bearer ${token}`
            };

            // Fetch roles, permissions, functions
            const [rolesRes, permsRes, funcsRes] = await Promise.all([
                fetch('http://localhost:5000/api/v2/auth/admin/roles', { headers }),
                fetch('http://localhost:5000/api/v2/auth/admin/permissions', { headers }),
                fetch('http://localhost:5000/api/v2/auth/admin/functions', { headers })
            ]);

            const rolesData = await rolesRes.json();
            const permsData = await permsRes.json();
            const funcsData = await funcsRes.json();

            if (rolesData.status === 'success') {
                // Fetch permissions for each role
                const rolesWithPerms = await Promise.all(
                    rolesData.data.map(async (role) => {
                        const permRes = await fetch(
                            `http://localhost:5000/api/v2/rbac/roles/${role.RoleID}/permissions`,
                            { headers }
                        );
                        const permData = await permRes.json();
                        return {
                            ...role,
                            permissions: permData.status === 'success' ? permData.data : []
                        };
                    })
                );
                setRoles(rolesWithPerms);
            }

            if (permsData.status === 'success') {
                setPermissions(permsData.data);
            }

            if (funcsData.status === 'success') {
                setFunctions(funcsData.data);
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleEditRole = (role) => {
        setSelectedRole(role);
        setTempPermissions(role.permissions.map(p => p.PermissionID));
        setIsModalOpen(true);
    };

    const handleTogglePermission = (permissionId) => {
        setTempPermissions(prev => {
            if (prev.includes(permissionId)) {
                return prev.filter(id => id !== permissionId);
            } else {
                return [...prev, permissionId];
            }
        });
    };

    const handleSavePermissions = async () => {
        setSaving(true);
        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch(
                `http://localhost:5000/api/v2/rbac/roles/${selectedRole.RoleID}/permissions`,
                {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        permission_ids: tempPermissions
                    })
                }
            );

            const data = await response.json();

            if (data.status === 'success') {
                // Refresh data
                await fetchData();
                setIsModalOpen(false);
                setSelectedRole(null);
            } else {
                alert('Lỗi: ' + data.message);
            }
        } catch (error) {
            console.error('Error saving permissions:', error);
            alert('Không thể lưu thay đổi');
        } finally {
            setSaving(false);
        }
    };

    const getFunctionsForPermission = (permissionId) => {
        // This would need an API call in real implementation
        // For now, return empty array
        return [];
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-slate-900 flex items-center justify-center">
                <div className="text-center">
                    <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-slate-400">Đang tải dữ liệu...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-900 p-6">
            {/* Header */}
            <div className="mb-8">
                <div className="flex items-center gap-3 mb-2">
                    <Shield className="text-blue-500" size={32} />
                    <h1 className="text-3xl font-bold text-white">Quản lý phân quyền</h1>
                </div>
                <p className="text-slate-400">Quản lý vai trò, quyền hạn và chức năng hệ thống</p>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-slate-400 text-sm mb-1">Tổng số vai trò</p>
                            <p className="text-3xl font-bold text-white">{roles.length}</p>
                        </div>
                        <div className="bg-blue-500/10 p-3 rounded-lg">
                            <Users className="text-blue-500" size={24} />
                        </div>
                    </div>
                </div>

                <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-slate-400 text-sm mb-1">Tổng số quyền</p>
                            <p className="text-3xl font-bold text-white">{permissions.length}</p>
                        </div>
                        <div className="bg-green-500/10 p-3 rounded-lg">
                            <Key className="text-green-500" size={24} />
                        </div>
                    </div>
                </div>

                <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-slate-400 text-sm mb-1">Tổng số chức năng</p>
                            <p className="text-3xl font-bold text-white">{functions.length}</p>
                        </div>
                        <div className="bg-purple-500/10 p-3 rounded-lg">
                            <Settings className="text-purple-500" size={24} />
                        </div>
                    </div>
                </div>
            </div>

            {/* Roles List */}
            <div className="bg-slate-800 rounded-lg border border-slate-700">
                <div className="p-6 border-b border-slate-700">
                    <h2 className="text-xl font-bold text-white">Danh sách vai trò</h2>
                </div>

                <div className="divide-y divide-slate-700">
                    {roles.map((role) => (
                        <div key={role.RoleID} className="p-6 hover:bg-slate-700/50 transition-colors">
                            <div className="flex items-start justify-between mb-4">
                                <div className="flex-1">
                                    <div className="flex items-center gap-3 mb-2">
                                        <h3 className="text-lg font-semibold text-white">{role.RoleName}</h3>
                                        <span className="px-2 py-1 bg-blue-500/10 text-blue-400 text-xs rounded-full">
                                            {role.permissions.length} quyền
                                        </span>
                                    </div>
                                    <p className="text-slate-400 text-sm">{role.Description}</p>
                                </div>
                                <button
                                    onClick={() => handleEditRole(role)}
                                    className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                                >
                                    <Edit size={16} />
                                    Chỉnh sửa
                                </button>
                            </div>

                            {/* Permissions */}
                            {role.permissions.length > 0 && (
                                <div>
                                    <p className="text-sm text-slate-400 mb-2">Quyền hạn:</p>
                                    <div className="flex flex-wrap gap-2">
                                        {role.permissions.map((perm) => (
                                            <div
                                                key={perm.PermissionID}
                                                className="px-3 py-1.5 bg-slate-700 text-slate-300 text-sm rounded-lg border border-slate-600"
                                            >
                                                {perm.PermissionName}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>

            {/* Edit Modal */}
            {isModalOpen && selectedRole && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm">
                    <div className="bg-slate-800 rounded-lg shadow-2xl w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col">
                        {/* Modal Header */}
                        <div className="flex items-center justify-between p-6 border-b border-slate-700">
                            <div>
                                <h2 className="text-2xl font-bold text-white">Chỉnh sửa quyền hạn</h2>
                                <p className="text-slate-400 text-sm mt-1">
                                    Vai trò: <span className="text-blue-400 font-medium">{selectedRole.RoleName}</span>
                                </p>
                            </div>
                            <button
                                onClick={() => setIsModalOpen(false)}
                                className="text-slate-400 hover:text-white transition-colors"
                            >
                                <X size={24} />
                            </button>
                        </div>

                        {/* Modal Body */}
                        <div className="flex-1 overflow-y-auto p-6">
                            <div className="space-y-3">
                                {permissions.map((permission) => {
                                    const isSelected = tempPermissions.includes(permission.PermissionID);

                                    return (
                                        <div
                                            key={permission.PermissionID}
                                            className={`p-4 rounded-lg border-2 transition-all cursor-pointer ${isSelected
                                                    ? 'bg-blue-500/10 border-blue-500'
                                                    : 'bg-slate-700/50 border-slate-600 hover:border-slate-500'
                                                }`}
                                            onClick={() => handleTogglePermission(permission.PermissionID)}
                                        >
                                            <div className="flex items-start justify-between">
                                                <div className="flex-1">
                                                    <div className="flex items-center gap-2 mb-1">
                                                        <h4 className="font-semibold text-white">{permission.PermissionName}</h4>
                                                        {isSelected && (
                                                            <Check className="text-blue-400" size={20} />
                                                        )}
                                                    </div>
                                                    <p className="text-sm text-slate-400">{permission.Description}</p>
                                                </div>
                                                <div className={`w-5 h-5 rounded border-2 flex items-center justify-center ${isSelected ? 'bg-blue-500 border-blue-500' : 'border-slate-500'
                                                    }`}>
                                                    {isSelected && <Check size={14} className="text-white" />}
                                                </div>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>

                        {/* Modal Footer */}
                        <div className="flex items-center justify-between p-6 border-t border-slate-700 bg-slate-800/50">
                            <div className="text-sm text-slate-400">
                                Đã chọn: <span className="text-white font-medium">{tempPermissions.length}</span> quyền
                            </div>
                            <div className="flex gap-3">
                                <button
                                    onClick={() => setIsModalOpen(false)}
                                    className="px-6 py-2.5 bg-slate-700 text-white rounded-lg hover:bg-slate-600 transition-colors"
                                >
                                    Hủy
                                </button>
                                <button
                                    onClick={handleSavePermissions}
                                    disabled={saving}
                                    className="px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                                >
                                    {saving ? (
                                        <>
                                            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
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
            )}
        </div>
    );
};

export default AccessControlPage;
