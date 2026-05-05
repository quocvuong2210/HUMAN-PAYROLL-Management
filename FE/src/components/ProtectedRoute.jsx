import { Navigate } from 'react-router-dom'

/**
 * ProtectedRoute Component
 * 
 * Bảo vệ routes dựa trên authentication và roles
 * 
 * @param {ReactNode} children - Component con cần bảo vệ
 * @param {Array<string>} requiredRoles - Danh sách roles được phép truy cập (optional)
 * 
 * Cách sử dụng:
 * 
 * 1. Chỉ kiểm tra đăng nhập:
 * <ProtectedRoute>
 *   <DashboardPage />
 * </ProtectedRoute>
 * 
 * 2. Kiểm tra đăng nhập + roles:
 * <ProtectedRoute requiredRoles={['SUPER_ADMIN', 'HR_MANAGER']}>
 *   <UserPage />
 * </ProtectedRoute>
 */
export default function ProtectedRoute({ children, requiredRoles = [] }) {
    const token = localStorage.getItem('access_token')
    const userRolesStr = localStorage.getItem('user_roles')

    // Kiểm tra đăng nhập
    if (!token) {
        return <Navigate to="/login" replace />
    }

    // Nếu có yêu cầu roles cụ thể
    if (requiredRoles.length > 0) {
        try {
            const userRoles = userRolesStr ? JSON.parse(userRolesStr) : []

            // Kiểm tra xem user có ít nhất 1 role trong danh sách requiredRoles không
            const hasRole = requiredRoles.some(role => userRoles.includes(role))

            if (!hasRole) {
                return <Navigate to="/403" replace />
            }
        } catch (error) {
            console.error('Error parsing user roles:', error)
            return <Navigate to="/login" replace />
        }
    }

    return children
}
