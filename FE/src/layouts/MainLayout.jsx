import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Header from '../components/Header';
import SideBar from '../components/Sidebar';

export default function MainLayout() {
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [language, setLanguage] = useState('vi'); 

  const toggleDarkMode = () => setIsDarkMode(!isDarkMode);

const toggleLanguage = () => {
  console.log("Đã gọi hàm đổi ngôn ngữ từ MainLayout!");
  setLanguage((prev) => {
    const newLang = prev === 'vi' ? 'en' : 'vi';
   
    return newLang;
  });
};

  return (
    <div className={`flex flex-col h-screen overflow-hidden transition-colors duration-300 ${isDarkMode ? 'bg-slate-950' : 'bg-slate-50'}`}>
      {/* Truyền thêm ngôn ngữ và hàm đổi vào Header */}
      <Header 
        isDarkMode={isDarkMode} 
        toggleDarkMode={toggleDarkMode} 
        language={language} 
        toggleLanguage={toggleLanguage} 
      />

      <div className="flex flex-1 overflow-hidden">
        <SideBar isDarkMode={isDarkMode} language={language} />

        <main className="flex-1 overflow-y-auto p-4">
          {/* TRUYỀN: Ngôn ngữ xuống các trang con qua Outlet */}
          <Outlet context={{ isDarkMode, language }} />
        </main>
      </div>
    </div>
  );
}