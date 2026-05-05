# UserPage.jsx Integration Patch

## Quick Integration Guide

Follow these steps to integrate the new `UserCreateModalWithRoles` component into your existing `UserPage.jsx`:

---

## Step 1: Add Import (Line ~10)

**Find this line:**
```jsx
import { 
  Users, UserPlus, Search, Edit2, Trash2, X, 
  Loader2, ChevronRight, CheckCircle2, Clock, Globe, 
  Monitor, AlertCircle, RefreshCw, Calendar, Mail, Phone, User,
  Shield, ChevronLeft, ChevronsLeft, ChevronsRight
} from 'lucide-react'
```

**Add this line after it:**
```jsx
import UserCreateModalWithRoles from '../components/UserCreateModalWithRoles'
```

---

## Step 2: Replace the Old Create User Modal (Around Line 618)

**Find this section:**
```jsx
      {/* Create User Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className={`w-full max-w-md rounded-2xl p-6 ${isDarkMode ? 'bg-slate-900' : 'bg-white'}`}>
            <div className="flex items-center justify-between mb-6">
              <h3 className={`text-lg font-bold ${isDarkMode ? 'text-white' : 'text-slate-800'}`}>{t.createUser}</h3>
              <button onClick={() => setShowModal(false)} className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800">
                <X size={18} />
              </button>
            </div>
            
            <div className="space-y-4">
              ... (lots of form fields)
            </div>

            <div className="flex gap-3 mt-6">
              <button 
                onClick={() => setShowModal(false)}
                ...
              >
                {t.cancel}
              </button>
              <button 
                onClick={handleCreateUser}
                ...
              >
                {t.save}
              </button>
            </div>
          </div>
        </div>
      )}
```

**Replace the ENTIRE section above with:**
```jsx
      {/* Create User Modal - New Version with Roles */}
      <UserCreateModalWithRoles
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        isDarkMode={isDarkMode}
        onSuccess={(data) => {
          console.log('User created successfully:', data)
          fetchUsers() // Refresh user list
        }}
      />
```

---

## Step 3: (Optional) Clean Up Old Code

### 3.1 Remove Old State (Around Line 120)

**Find and remove (or comment out):**
```jsx
  const [newUserForm, setNewUserForm] = useState({
    username: '',
    email: '',
    password: '',
    phone: '',
    dob: '',
    gender: 'Nam'
  })
```

### 3.2 Remove Old Handler Function (Around Line 216)

**Find and remove (or comment out):**
```jsx
  const handleCreateUser = async () => {
    try {
      // Convert empty string to null for date fields
      const payload = {
        username: newUserForm.username || null,
        email: newUserForm.email || null,
        password: newUserForm.password || null,
        phone: newUserForm.phone || null,
        dob: newUserForm.dob && newUserForm.dob.trim() !== '' ? newUserForm.dob : null,
        gender: newUserForm.gender || null
      }
      
      const res = await fetch(`${API_BASE}/api/v1/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      const data = await res.json()
      if (data.status === 'success') {
        fetchUsers()
        setShowModal(false)
        setNewUserForm({
          username: '',
          email: '',
          password: '',
          phone: '',
          dob: '',
          gender: 'Nam'
        })
      } else {
        alert(data.message)
      }
    } catch (err) {
      alert('Error creating user')
    }
  }
```

---

## Complete Example

Here's what the relevant sections should look like after integration:

### Imports Section:
```jsx
import React, { useState, useEffect, useCallback } from 'react'
import { useOutletContext } from 'react-router-dom'
import { 
  Users, UserPlus, Search, Edit2, Trash2, X, 
  Loader2, ChevronRight, CheckCircle2, Clock, Globe, 
  Monitor, AlertCircle, RefreshCw, Calendar, Mail, Phone, User,
  Shield, ChevronLeft, ChevronsLeft, ChevronsRight
} from 'lucide-react'
import UserCreateModalWithRoles from '../components/UserCreateModalWithRoles'  // ← NEW

const API_BASE = import.meta.env.VITE_API_URL
```

### Modal Section (at the end of component, before closing div):
```jsx
      {/* Create User Modal - New Version with Roles */}
      <UserCreateModalWithRoles
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        isDarkMode={isDarkMode}
        onSuccess={(data) => {
          console.log('User created successfully:', data)
          fetchUsers() // Refresh user list
        }}
      />

      {/* Edit User Modal */}
      {showEditModal && (
        ... existing edit modal code ...
      )}
    </div>
  )
}
```

---

## Testing After Integration

1. **Start Backend:**
   ```bash
   cd BE
   python app.py
   ```

2. **Start Frontend:**
   ```bash
   cd FE
   pnpm run dev
   ```

3. **Test the Flow:**
   - Navigate to User Management page
   - Click "Thêm Người Dùng" button
   - You should see the new modal with role selection
   - Fill in the form and select roles
   - Click "Tạo người dùng"
   - Check console for success message
   - User list should refresh automatically

4. **Verify in Database:**
   ```sql
   -- Check user was created
   SELECT * FROM [USER] WHERE Username = 'your_test_username'
   
   -- Check roles were assigned
   SELECT U.Username, R.RoleName
   FROM [USER] U
   INNER JOIN [USER_ROLE] UR ON U.UserID = UR.UserID
   INNER JOIN [ROLE] R ON UR.RoleID = R.RoleID
   WHERE U.Username = 'your_test_username'
   
   -- Check verification token was created
   SELECT * FROM [EmailVerification] WHERE UserID = (
     SELECT UserID FROM [USER] WHERE Username = 'your_test_username'
   )
   
   -- Check activity was logged
   SELECT * FROM [UserAccessLog] WHERE Action = 'CREATE_USER'
   ORDER BY AccessTime DESC
   ```

---

## Troubleshooting

### Modal doesn't appear
- Check browser console for errors
- Verify `UserCreateModalWithRoles.jsx` exists in `FE/src/components/`
- Check import path is correct

### Roles don't load
- Check backend is running
- Verify `/api/v1/auth/roles` endpoint returns data
- Check browser Network tab for API call

### User creation fails
- Check backend logs for errors
- Verify database connection
- Check all required tables exist (USER, ROLE, USER_ROLE, EmailVerification, UserAccessLog)

### Form validation errors
- Email must be valid format: `user@example.com`
- Password must be at least 6 characters
- Username must be at least 3 characters

---

## Success Indicators

✅ Modal opens with role selection checkboxes
✅ Roles load from backend
✅ Form validation works
✅ User is created with Status='INACTIVE'
✅ Roles are assigned to user
✅ Verification token is generated
✅ Activity is logged
✅ User list refreshes automatically
✅ Success message appears
✅ Modal closes after creation

---

## Need Help?

If you encounter any issues:

1. Check `RBAC_IMPLEMENTATION_COMPLETE.md` for detailed documentation
2. Review backend logs for error messages
3. Check browser console for frontend errors
4. Verify database schema matches `BE/database/rbac_system.sql`
5. Ensure all dependencies are installed:
   - Backend: `pip install -r BE/requirement.txt`
   - Frontend: `cd FE && pnpm install`

---

**That's it! You're done! 🎉**

The new user creation modal with role selection is now integrated into your UserPage.

