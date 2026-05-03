import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { User, Mail, Phone, Calendar, ShieldCheck, Edit3, Save, X, History } from 'lucide-react';

const API_BASE = `${import.meta.env.VITE_API_URL}/api/v1/auth`;

export default function ProfilePage() {
  const [user, setUser] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({});

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const token = localStorage.getItem('accessToken');
      const res = await axios.get(`${API_BASE}/profile`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUser(res.data.data);
      setFormData(res.data.data);
    } catch (err) { console.error("Lỗi tải profile", err); }
  };

  const handleUpdate = async () => {
    try {
      const token = localStorage.getItem('accessToken');
      await axios.put(`${API_BASE}/users/${user.UserID}`, formData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setIsEditing(false);
      fetchProfile();
      alert("Cập nhật thành công!");
    } catch (err) { alert("Lỗi cập nhật!"); }
  };

  if (!user) return <div className="text-white p-10">Đang tải...</div>;

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-6 animate-in fade-in duration-500">
      {/* HEADER CARD */}
      <div className="bg-slate-900/50 backdrop-blur-xl p-8 rounded-[2rem] border border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <div className="w-20 h-20 bg-blue-600 rounded-3xl flex items-center justify-center text-3xl font-black text-white shadow-lg shadow-blue-500/20">
            {user.Username.charAt(0).toUpperCase()}
          </div>
          <div>
            <h1 className="text-2xl font-black text-white uppercase">{user.Username}</h1>
            <span className="text-blue-500 text-xs font-bold uppercase tracking-widest">{user.Status}</span>
          </div>
        </div>
        <button 
          onClick={() => setIsEditing(!isEditing)}
          className="flex items-center gap-2 px-6 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-bold text-sm transition-all"
        >
          {isEditing ? <><X size={16}/> Hủy</> : <><Edit3 size={16}/> Chỉnh sửa</>}
        </button>
      </div>

      {/* FORM CHI TIẾT */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-slate-900/50 p-6 rounded-[2rem] border border-slate-800 space-y-4">
          <h3 className="text-[11px] font-black uppercase text-slate-500 mb-4 flex items-center gap-2">
            <User size={14}/> Thông tin cá nhân
          </h3>
          
          {[
            { label: 'Email', key: 'Email', icon: Mail },
            { label: 'Số điện thoại', key: 'PhoneNumber', icon: Phone },
            { label: 'Ngày sinh', key: 'DateOfBirth', icon: Calendar },
          ].map((field) => (
            <div key={field.key}>
              <label className="text-[9px] font-bold text-slate-600 uppercase ml-1">{field.label}</label>
              {isEditing ? (
                <input 
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-white text-sm outline-none focus:border-blue-500"
                  value={formData[field.key] || ''}
                  onChange={(e) => setFormData({...formData, [field.key]: e.target.value})}
                />
              ) : (
                <p className="p-3 text-sm font-medium text-slate-300">{user[field.key] || 'Chưa cập nhật'}</p>
              )}
            </div>
          ))}
          
          {isEditing && (
            <button onClick={handleUpdate} className="w-full py-3 bg-blue-600 rounded-xl text-white font-black flex items-center justify-center gap-2">
              <Save size={16}/> Lưu thay đổi
            </button>
          )}
        </div>

        {/* LỊCH SỬ TRUY CẬP */}
        <div className="bg-slate-900/50 p-6 rounded-[2rem] border border-slate-800">
          <h3 className="text-[11px] font-black uppercase text-slate-500 mb-4 flex items-center gap-2">
            <History size={14}/> Lịch sử truy cập gần đây
          </h3>
          <div className="space-y-3">
            {user.access_history.map((log, i) => (
              <div key={i} className="flex justify-between items-center p-3 border border-slate-800 rounded-xl">
                <div>
                  <p className="text-xs font-bold text-blue-500">{log.Action}</p>
                  <p className="text-[10px] text-slate-500">{new Date(log.AccessTime).toLocaleString()}</p>
                </div>
                <span className="text-[9px] font-mono text-slate-600">{log.IPAddress}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}