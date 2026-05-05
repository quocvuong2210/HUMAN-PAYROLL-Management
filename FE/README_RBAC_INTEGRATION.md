# 🎨 RBAC Frontend Integration Guide

## 📦 Installation

```bash
cd FE
pnpm install
# hoặc
npm install
```

**Dependencies mới:**
- `react-select`: ^5.8.0 - Multi-select dropdown cho roles

---

## 🗂️ File Structure

```
FE/src/
├── components/
│   └── UserCreateModal.jsx       # Modal tạo user với role selection
├── pages/
│   ├── AccessControlPage.jsx     # Trang quản lý RBAC
│   └── UserPage.jsx               # Trang danh sách users với role badges
└── ...
```

---

## 🚀 Quick Start

### 1. Import Components

```jsx
import UserCreateModal from './components/UserCreateModal';
import AccessControlPage from './pages/AccessControlPage';
import UserPage from './pages/UserPage';
```

### 2. Setup Routes

```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/users" element={<UserPage />} />
        <Route path="/access-control" element={<AccessControlPage />} />
      </Routes>
    </BrowserRouter>
  );
}
```

### 3. Configure API Base URL

Trong các component, update base URL nếu cần:

```jsx
const API_BASE_URL = 'http://localhost:5000/api/v2';
```

---

## 📝 Component Usage

### UserCreateModal

Modal để tạo user mới với role selection.

**Props:**
- `isOpen` (boolean): Hiển thị/ẩn modal
- `onClose` (function): Callback khi đóng modal
- `onSuccess` (function): Callback khi tạo user thành công

**Example:**
```jsx
import { useState } from 'react';
import UserCreateModal from './components/UserCreateModal';

function MyComponent() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleSuccess = (data) => {
    console.log('User created:', data);
    // Refresh user list
  };

  return (
    <>
      <button onClick={() => setIsModalOpen(true)}>
        Tạo người dùng
      </button>

      <UserCreateModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={handleSuccess}
      />
    </>
  );
}
```

**Features:**
- ✅ Multi-select roles với react-select
- ✅ Form validation
- ✅ Dark mode styling
- ✅ Loading states
- ✅ Error handling
- ✅ Responsive design

---

### AccessControlPage

Trang quản lý phân quyền (RBAC).

**Features:**
- ✅ Hiển thị danh sách roles
- ✅ Xem permissions của từng role
- ✅ Chỉnh sửa permissions (modal)
- ✅ Toggle permissions on/off
- ✅ Statistics cards
- ✅ Dark mode UI

**Example:**
```jsx
import AccessControlPage from './pages/AccessControlPage';

function App() {
  return <AccessControlPage />;
}
```

**API Endpoints Used:**
- `GET /api/v2/auth/admin/roles`
- `GET /api/v2/auth/admin/permissions`
- `GET /api/v2/auth/admin/functions`
- `GET /api/v2/rbac/roles/{id}/permissions`
- `PUT /api/v2/rbac/roles/{id}/permissions`

---

### UserPage

Trang danh sách users với role badges.

**Features:**
- ✅ Hiển thị danh sách users
- ✅ Role badges với màu sắc
- ✅ Search functionality
- ✅ Statistics cards
- ✅ User actions (edit, delete)
- ✅ Integration với UserCreateModal

**Example:**
```jsx
import UserPage from './pages/UserPage';

function App() {
  return <UserPage />;
}
```

**API Endpoints Used:**
- `GET /api/v2/users`
- `GET /api/v2/auth/admin/users/{id}/roles`
- `POST /api/v2/users/create`

---

## 🎨 Styling

### Dark Mode Theme

Tất cả components sử dụng Tailwind CSS với dark mode palette:

```css
/* Main colors */
bg-slate-900    /* Background */
bg-slate-800    /* Cards */
bg-slate-700    /* Inputs */
text-white      /* Primary text */
text-slate-400  /* Secondary text */

/* Accent colors */
bg-blue-600     /* Primary buttons */
bg-red-500      /* Danger */
bg-green-500    /* Success */
```

### Role Badge Colors

```jsx
const getRoleBadgeColor = (roleName) => {
  const colors = {
    'ADMIN': 'bg-red-500/10 text-red-400 border-red-500/20',
    'HR_MANAGER': 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    'EMPLOYEE': 'bg-green-500/10 text-green-400 border-green-500/20',
    'VIEWER': 'bg-gray-500/10 text-gray-400 border-gray-500/20'
  };
  return colors[roleName] || 'bg-slate-500/10 text-slate-400 border-slate-500/20';
};
```

---

## 🔐 Authentication

### Token Management

Tất cả API calls yêu cầu Bearer token:

```jsx
const token = localStorage.getItem('access_token');

fetch('http://localhost:5000/api/v2/users', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

### Token Storage

```jsx
// Lưu token sau khi login
localStorage.setItem('access_token', token);
localStorage.setItem('refresh_token', refreshToken);

// Lấy token
const token = localStorage.getItem('access_token');

// Xóa token khi logout
localStorage.removeItem('access_token');
localStorage.removeItem('refresh_token');
```

---

## 📡 API Integration

### Example: Fetch Users

```jsx
const fetchUsers = async () => {
  try {
    const token = localStorage.getItem('access_token');
    const response = await fetch('http://localhost:5000/api/v2/users', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    const data = await response.json();
    
    if (data.status === 'success') {
      setUsers(data.data);
    }
  } catch (error) {
    console.error('Error fetching users:', error);
  }
};
```

### Example: Create User with Roles

```jsx
const createUser = async (userData) => {
  try {
    const token = localStorage.getItem('access_token');
    const response = await fetch('http://localhost:5000/api/v2/users/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        username: userData.username,
        email: userData.email,
        password: userData.password,
        roles: userData.roles.map(r => r.value) // [1, 2, 3]
      })
    });
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error creating user:', error);
  }
};
```

### Example: Update Role Permissions

```jsx
const updateRolePermissions = async (roleId, permissionIds) => {
  try {
    const token = localStorage.getItem('access_token');
    const response = await fetch(
      `http://localhost:5000/api/v2/rbac/roles/${roleId}/permissions`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          permission_ids: permissionIds
        })
      }
    );
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error updating permissions:', error);
  }
};
```

---

## 🎯 Features Checklist

### UserCreateModal
- [x] Username input
- [x] Email input
- [x] Password input
- [x] Phone number input
- [x] Date of birth picker
- [x] Gender select
- [x] Multi-select roles (react-select)
- [x] Form validation
- [x] Error handling
- [x] Loading states
- [x] Dark mode styling

### AccessControlPage
- [x] Display all roles
- [x] Show permissions per role
- [x] Edit permissions modal
- [x] Toggle permissions
- [x] Statistics cards
- [x] Save changes
- [x] Loading states
- [x] Error handling

### UserPage
- [x] Display users list
- [x] Show role badges
- [x] Search functionality
- [x] Statistics cards
- [x] Create user button
- [x] Edit/Delete actions
- [x] Status badges
- [x] Responsive table

---

## 🐛 Troubleshooting

### Issue: react-select not styled correctly

**Solution:**
```bash
pnpm install react-select
```

Ensure custom styles are applied:
```jsx
const selectStyles = {
  control: (base) => ({
    ...base,
    backgroundColor: '#1e293b',
    borderColor: '#334155'
  }),
  // ... other styles
};

<Select styles={selectStyles} />
```

### Issue: CORS errors

**Solution:**
Backend đã có CORS enabled. Nếu vẫn lỗi, check:
```python
# BE/app.py
from flask_cors import CORS
CORS(app)
```

### Issue: 401 Unauthorized

**Solution:**
Check token:
```jsx
const token = localStorage.getItem('access_token');
console.log('Token:', token);

// Nếu token hết hạn, refresh:
const refreshToken = async () => {
  const refresh = localStorage.getItem('refresh_token');
  const response = await fetch('/api/v2/auth/refresh-token', {
    method: 'POST',
    body: JSON.stringify({ refresh_token: refresh })
  });
  const data = await response.json();
  localStorage.setItem('access_token', data.access_token);
};
```

### Issue: 403 Forbidden

**Solution:**
User không có quyền. Check permissions:
```jsx
// Fetch user permissions
const response = await fetch('/api/v2/auth/me/permissions', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const data = await response.json();
console.log('User permissions:', data.data.permissions);
```

---

## 📱 Responsive Design

Tất cả components đều responsive:

```jsx
// Mobile: 1 column
// Tablet: 2 columns
// Desktop: 3 columns
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
```

---

## 🎨 Customization

### Change Colors

```jsx
// Update Tailwind classes
className="bg-blue-600"  // Change to bg-purple-600
className="text-blue-400" // Change to text-purple-400
```

### Change Icons

```jsx
import { Users, Shield, Key } from 'lucide-react';

// Replace with other lucide-react icons
import { Star, Heart, Bell } from 'lucide-react';
```

### Add New Fields

```jsx
// In UserCreateModal.jsx
<div>
  <label>Department</label>
  <select name="department" onChange={handleChange}>
    <option value="IT">IT</option>
    <option value="HR">HR</option>
  </select>
</div>
```

---

## 🚀 Deployment

### Build for Production

```bash
pnpm run build
```

### Environment Variables

Create `.env` file:
```env
VITE_API_BASE_URL=https://your-api.com/api/v2
```

Use in code:
```jsx
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
```

---

## 📚 Additional Resources

- [React Select Documentation](https://react-select.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Lucide React Icons](https://lucide.dev/)
- [Backend API Documentation](../BE/docs/USER_MANAGEMENT_API.md)

---

## 💡 Best Practices

1. **Always validate user input** before sending to API
2. **Handle loading states** for better UX
3. **Show error messages** clearly to users
4. **Cache API responses** when appropriate
5. **Use optimistic updates** for better perceived performance
6. **Implement proper error boundaries**
7. **Add loading skeletons** for better UX
8. **Use debounce** for search inputs
9. **Implement pagination** for large lists
10. **Add confirmation dialogs** for destructive actions

---

## 🎉 You're Ready!

Hệ thống RBAC frontend đã sẵn sàng. Chạy development server:

```bash
pnpm run dev
```

Navigate to:
- `/users` - User management page
- `/access-control` - RBAC management page
