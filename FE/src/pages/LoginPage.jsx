import React, { useState } from 'react';
import { Lock, User, AlertCircle, ArrowRight, ShieldCheck, Loader2 } from 'lucide-react';

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
                localStorage.setItem('accessToken', data.token);
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
        <div className="min-h-screen flex items-center justify-center bg-slate-950 p-6 font-sans">
            {/* Background Decorative Elements */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
                <div className="absolute -top-[20%] -left-[10%] w-[500px] h-[500px] bg-blue-600/20 rounded-full blur-[120px]" />
                <div className="absolute bottom-[0%] right-[0%] w-[400px] h-[400px] bg-indigo-600/20 rounded-full blur-[100px]" />
            </div>

            {/* Login Card */}
            <div className="w-full max-w-[420px] relative z-10">
                <div className="bg-slate-900/50 backdrop-blur-2xl border border-slate-800 p-8 rounded-[2rem] shadow-2xl">
                    
                    {/* Brand Header */}
                    <div className="flex flex-col items-center mb-10">
                        <div className="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-600/20 mb-4">
                            <ShieldCheck size={32} className="text-white" />
                        </div>
                        <h2 className="text-2xl font-black text-white tracking-tight uppercase">HR System</h2>
                        <p className="text-slate-400 text-xs font-bold uppercase tracking-widest mt-1">Quản trị truy cập</p>
                    </div>

                    <form onSubmit={handleLogin} className="space-y-5">
                        {error && (
                            <div className="flex items-center gap-2 bg-rose-500/10 text-rose-400 p-3 rounded-xl border border-rose-500/20 text-[11px] font-bold uppercase">
                                <AlertCircle size={16} /> {error}
                            </div>
                        )}

                        {/* Username Input */}
                        <div className="space-y-1.5">
                            <label className="text-[10px] font-black text-slate-500 uppercase ml-1">Username</label>
                            <div className="relative group">
                                <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-blue-500 transition-colors" size={18} />
                                <input
                                    type="text"
                                    className="w-full bg-slate-950 border border-slate-800 rounded-xl py-3.5 pl-12 pr-4 text-white text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
                                    placeholder="Nhập tên đăng nhập..."
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    required
                                />
                            </div>
                        </div>

                        {/* Password Input */}
                        <div className="space-y-1.5">
                            <label className="text-[10px] font-black text-slate-500 uppercase ml-1">Password</label>
                            <div className="relative group">
                                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-blue-500 transition-colors" size={18} />
                                <input
                                    type="password"
                                    className="w-full bg-slate-950 border border-slate-800 rounded-xl py-3.5 pl-12 pr-4 text-white text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all"
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
                            className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-500 text-white font-black py-3.5 rounded-xl transition-all active:scale-[0.98] mt-4"
                        >
                            {loading ? <Loader2 className="animate-spin" size={20} /> : (
                                <>
                                    Đăng nhập <ArrowRight size={18} />
                                </>
                            )}
                        </button>
                    </form>
                </div>

            
            </div>
        </div>
    );
}