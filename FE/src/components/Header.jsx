import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Search, Bell, Moon, Sun, ChevronDown } from 'lucide-react';

export default function Header({ isDarkMode, toggleDarkMode, language, toggleLanguage }) {
  const isVi = language === 'vi';
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState(null);

  // 1. Hàm lấy dữ liệu Profile từ API
  const fetchProfile = useCallback(async () => {
    const API_BASE = "http://localhost:5000/api/v1";
  
    const token = localStorage.getItem('accessToken'); 

    try {
      const response = await axios.get(`${API_BASE}/auth/profile`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      // Set dữ liệu dựa trên cấu trúc JSON bạn cung cấp
      setUserData(response.data.data);
    } catch (err) {
      console.error("Lỗi lấy Profile:", err);
      setError(isVi ? "Lỗi tải thông tin" : "Failed to load profile");
    }
  }, [isVi]);

  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  // 2. Xử lý hiển thị tên và Label
  const displayName = userData?.profile?.username || (isVi ? 'Khách' : 'Guest');
  const userLabel = userData?.lbac_info?.label || 'General';

  return (
    <div className={`h-16 flex items-center justify-between px-6 shadow-sm border-b transition-all duration-300 z-50 relative ${
      isDarkMode ? 'bg-[#1e1e2d] border-slate-800' : 'bg-white border-slate-200'
    }`}>
      
      {/* LEFT SIDE: Language & Theme */}
      <div className="flex items-center gap-1 z-10">
        <div 
          onClick={toggleLanguage}
          className={`flex items-center gap-2 px-3 py-1.5 rounded-xl cursor-pointer transition-all border border-transparent ${
            isDarkMode ? 'hover:bg-slate-800 hover:border-slate-700 text-slate-300' : 'hover:bg-slate-50 hover:border-slate-100 text-slate-600'
          }`}
        >
          <img 
            src={isVi ? "https://flagcdn.com/w20/vn.png" : "https://flagcdn.com/w20/us.png"} 
            alt="Flag" 
            className="w-5 h-3.5 object-cover rounded-sm shadow-sm" 
          />
          <span className="text-xs font-bold uppercase tracking-wider">{isVi ? 'VN' : 'EN'}</span>
          <ChevronDown size={14} className="opacity-50" />
        </div>

        <button 
          onClick={toggleDarkMode}
          className={`p-2.5 rounded-xl transition-all duration-500 ${
            isDarkMode ? 'bg-slate-800 text-yellow-400 border border-slate-700' : 'bg-slate-100 text-slate-600 border border-slate-200'
          }`}
        >
          {isDarkMode ? <Sun size={18} /> : <Moon size={18} />}
        </button>
      </div>

      {/* CENTER SIDE: Project Title */}
      <div className="absolute left-1/2 -translate-x-1/2 hidden md:block">
        <span className="text-xl font-black tracking-tighter bg-gradient-to-r from-indigo-600 via-violet-500 to-purple-500 bg-clip-text text-transparent uppercase italic">
          System Integration 2026
        </span>
      </div>

      {/* RIGHT SIDE: Profile & Actions */}
      <div className="flex items-center gap-3 z-10">
        
        <div className={`p-2 rounded-xl cursor-pointer transition-colors ${isDarkMode ? 'hover:bg-slate-800 text-slate-400' : 'hover:bg-slate-50 text-slate-500'}`}>
          <Search size={19} />
        </div>

        <div className="relative p-2.5 rounded-xl cursor-pointer transition-colors hover:bg-indigo-50 dark:hover:bg-slate-800 group">
          <Bell size={20} className="text-slate-400 group-hover:text-indigo-500" />
          <span className="absolute top-2 right-2 bg-rose-500 text-[9px] font-bold text-white w-4 h-4 flex items-center justify-center rounded-full border-2 border-white dark:border-[#1e1e2d] animate-pulse">
            5
          </span>
        </div>

        {/* USER PROFILE DYNAMIC DATA */}
        <div className={`flex items-center gap-3 ml-2 pl-4 border-l transition-colors ${isDarkMode ? 'border-slate-700' : 'border-slate-200'}`}>
          <div className="text-right hidden sm:block">
            <p className={`text-sm font-extrabold leading-tight tracking-tight ${isDarkMode ? 'text-slate-200' : 'text-slate-800'}`}>
               {displayName}
            </p>
            <div className="flex items-center justify-end gap-1.5">
               <p className="text-[10px] font-bold text-indigo-500 uppercase tracking-widest">
                  {userLabel}
               </p>
               <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
            </div>
          </div>
          
          <div className="relative group cursor-pointer">
            <img 
              src={`https://ui-avatars.com/api/?name=${displayName}&background=6366f1&color=fff`} 
              alt="Avatar" 
              className="w-10 h-10 rounded-xl border-2 border-indigo-500 p-0.5 transition-transform group-hover:scale-105 shadow-md"
            />
          </div>
        </div>
      </div>
    </div>
  );
}