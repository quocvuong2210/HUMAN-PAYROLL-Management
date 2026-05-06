import React, { useState } from 'react';
import { Lock, User, AlertCircle, ArrowRight, ShieldCheck, Loader2 } from 'lucide-react';
import bgImage from '../images/background.jpg';
export default function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            const response = await fetch('http://localhost:5000/api/v1/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });
            const data = await response.json();
            if (data.status === 'success') {
                // Lưu access token
                localStorage.setItem('accessToken', data.token);
                localStorage.setItem('access_token', data.token);

                // Lưu user info nếu có
                if (data.user) {
                    // Lưu roles
                    if (data.user.roles) {
                        localStorage.setItem('user_roles', JSON.stringify(data.user.roles));
                    }

                    // Lưu permissions
                    if (data.user.permissions) {
                        localStorage.setItem('user_permissions', JSON.stringify(data.user.permissions));
                    }

                    // Lưu functions
                    if (data.user.functions) {
                        localStorage.setItem('user_functions', JSON.stringify(data.user.functions));
                    }

                    // Lưu user info
                    localStorage.setItem('user_info', JSON.stringify({
                        userId: data.user.userId,
                        username: data.user.username,
                        email: data.user.email
                    }));
                }

                // Redirect to home
                window.location.href = '/';
            } else {
                setError(data.message || 'Sai tài khoản hoặc mật khẩu');
            }
        } catch (err) {
            setError('Không thể kết nối đến máy chủ');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div 
  className="min-h-screen flex items-center justify-center p-6 font-sans relative overflow-hidden"
  style={{
    backgroundImage: `url(${bgImage})`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    backgroundRepeat: "no-repeat"
  }}
>
  {/* Đảm bảo có một lớp phủ tối để chữ dễ đọc hơn */}
            <div className="absolute inset-0 bg-black/50" />

            {/* Login Card */}
            <div className="w-full max-w-md relative z-10">
                <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800/50 p-10 rounded-3xl shadow-2xl shadow-black/50">

                    {/* Brand Header */}
                    <div className="flex flex-col items-center mb-8">
                        <div className="relative mb-5">
                            <div className="absolute inset-0 bg-blue-600/20 rounded-2xl blur-xl"></div>
                            <div className="relative w-20 h-20 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-600/30">
                                <ShieldCheck size={40} className="text-white" />
                            </div>
                        </div>
                        <h2 className="text-3xl font-black text-white tracking-tight uppercase bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
                            HR System
                        </h2>
                        <p className="text-slate-400 text-xs font-bold uppercase tracking-[0.2em] mt-2">Quản trị truy cập</p>
                    </div>

                    <form onSubmit={handleLogin} className="space-y-4">
                        {error && (
                            <div className="flex items-center gap-2.5 bg-rose-500/10 text-rose-400 p-4 rounded-xl border border-rose-500/20 text-xs font-bold animate-in slide-in-from-top-2">
                                <AlertCircle size={18} className="flex-shrink-0" />
                                <span>{error}</span>
                            </div>
                        )}

                        {/* Username Input */}
                        <div className="space-y-2">
                            <label className="text-[11px] font-black text-slate-400 uppercase tracking-wider ml-1">Username</label>
                            <div className="relative group">
                                <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-blue-400 transition-all duration-300" size={20} />
                                <input
                                    type="text"
                                    className="w-full bg-slate-950/50 border border-slate-700/50 rounded-xl py-4 pl-12 pr-4 text-white text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all duration-300 placeholder:text-slate-600"
                                    placeholder="Nhập tên đăng nhập..."
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    required
                                />
                            </div>
                        </div>

                        {/* Password Input */}
                        <div className="space-y-2">
                            <label className="text-[11px] font-black text-slate-400 uppercase tracking-wider ml-1">Password</label>
                            <div className="relative group">
                                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-blue-400 transition-all duration-300" size={20} />
                                <input
                                    type="password"
                                    className="w-full bg-slate-950/50 border border-slate-700/50 rounded-xl py-4 pl-12 pr-4 text-white text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all duration-300 placeholder:text-slate-600"
                                    placeholder="••••••••"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                />
                            </div>
                        </div>

                        {/* Submit Button */}
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full flex items-center justify-center gap-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-black py-4 rounded-xl transition-all duration-300 active:scale-[0.98] shadow-lg shadow-blue-600/30 disabled:opacity-50 disabled:cursor-not-allowed mt-6"
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="animate-spin" size={20} />
                                    <span>Đang xử lý...</span>
                                </>
                            ) : (
                                <>
                                    <span>Login</span>
                                    <ArrowRight size={20} />
                                </>
                            )}
                        </button>
                    </form>

                    {/* Footer */}
                    <div className="mt-8 text-center">
                        <p className="text-xs text-slate-500">
                            Hệ thống quản lý nhân sự
                        </p>
                      
                    </div>
                </div>
            </div>
        </div>
    );
}