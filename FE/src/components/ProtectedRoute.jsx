import React from 'react';
import { Navigate } from 'react-router-dom';
import { jwtDecode } from "jwt-decode"; // Bạn cần cài lệnh: npm install jwt-decode

const ProtectedRoute = ({ children }) => {
    const token = localStorage.getItem('accessToken');

    if (!token) {
        // Không có token -> Về trang login
        return <Navigate to="/login" replace />;
    }

    try {
        // Giải mã token để kiểm tra thời gian hết hạn (exp)
        const decoded = jwtDecode(token);
        const currentTime = Date.now() / 1000; // Đổi ra giây

        if (decoded.exp < currentTime) {
            
            localStorage.removeItem('accessToken');
            alert("Phiên đăng nhập đã hết hạn, vui lòng đăng nhập lại!");
            return <Navigate to="/login" replace />;
        }

      
        return children;
    } catch (error) {
        // Token lỗi/không đúng định dạng
        localStorage.removeItem('accessToken');
        return <Navigate to="/login" replace />;
    }
};

export default ProtectedRoute;