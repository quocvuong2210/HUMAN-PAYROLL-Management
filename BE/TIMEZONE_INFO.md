# ⏰ THÔNG TIN TIMEZONE - NHẬT KÝ TRUY CẬP

## 🌍 Timezone Hiện Tại

### Backend (SQL Server)
- **Timezone**: Server timezone (có thể là UTC hoặc local)
- **Lưu vào database**: `GETDATE()` - Thời gian server
- **Column**: `AccessTime DATETIME DEFAULT GETDATE()`

### Frontend (React)
- **Nhận từ API**: String datetime từ backend
- **Convert**: `new Date(dateStr)` - Tự động convert sang timezone local của browser
- **Hiển thị**: `toLocaleString('vi-VN')` - Format theo giờ Việt Nam

## 📊 Ví Dụ

### Thời gian trong database:
```
2026-05-06 16:56:31.713  (Server time)
```

### Thời gian hiển thị trên frontend:
```
23:56:31 06/05/2026  (Browser time = Server time + timezone offset)
```

Nếu server ở UTC (GMT+0) và browser ở Việt Nam (GMT+7):
- Server: 16:56:31
- Browser: 23:56:31 (16:56:31 + 7 giờ)

## ✅ Tại Sao Thời Gian "Giống Nhau"?

Thời gian **KHÔNG GIỐNG NHAU** - Chúng khác nhau về giây:

| Log | Thời gian | Chênh lệch |
|-----|-----------|------------|
| 1 | 23:56:31 | - |
| 2 | 23:54:46 | -1 phút 45 giây |
| 3 | 23:52:34 | -2 phút 12 giây |
| 4 | 23:45:52 | -6 phút 42 giây |

Mỗi lần đăng nhập có thời gian **CHÍNH XÁC** đến từng giây!

## 🔧 Nếu Muốn Hiển Thị Rõ Hơn

### Option 1: Hiển thị milliseconds
```javascript
const formatDateTime = (dateStr) => {
    if (!dateStr) return 'N/A'
    const date = new Date(dateStr)
    return date.toLocaleString('vi-VN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        fractionalSecondDigits: 3  // Hiển thị milliseconds
    })
}
```

### Option 2: Hiển thị relative time
```javascript
const formatDateTime = (dateStr) => {
    if (!dateStr) return 'N/A'
    const date = new Date(dateStr)
    const now = new Date()
    const diff = now - date
    
    const seconds = Math.floor(diff / 1000)
    const minutes = Math.floor(seconds / 60)
    const hours = Math.floor(minutes / 60)
    const days = Math.floor(hours / 24)
    
    if (seconds < 60) return `${seconds} giây trước`
    if (minutes < 60) return `${minutes} phút trước`
    if (hours < 24) return `${hours} giờ trước`
    if (days < 7) return `${days} ngày trước`
    
    return date.toLocaleString('vi-VN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    })
}
```

## 🎯 Kết Luận

✅ **Thời gian KHÔNG giống nhau** - Mỗi log có timestamp riêng
✅ **Timezone đang hoạt động đúng** - Convert từ server time sang local time
✅ **Format đang đúng** - Hiển thị đầy đủ ngày/giờ/phút/giây

Nếu muốn thấy rõ hơn, có thể:
1. Thêm milliseconds vào format
2. Hiển thị "X phút trước" thay vì timestamp
3. Highlight log mới nhất bằng màu khác
