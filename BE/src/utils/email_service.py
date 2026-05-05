"""
Email Service - Gửi email xác nhận và reset password
Sử dụng SMTP hoặc mock cho development
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailService:
    def __init__(self):
        # Cấu hình SMTP (Lấy từ environment variables)
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_user = os.getenv('SMTP_USER', 'your-email@gmail.com')
        self.smtp_password = os.getenv('SMTP_PASSWORD', 'your-app-password')
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@yourcompany.com')
        self.mock_mode = os.getenv('EMAIL_MOCK_MODE', 'True') == 'True'
        
    def send_verification_email(self, to_email, username, token):
        """
        Gửi email xác nhận đăng ký
        
        Args:
            to_email: Email người nhận
            username: Tên người dùng
            token: Token xác nhận
        """
        subject = "Xác nhận đăng ký tài khoản"
        
        # URL xác nhận (thay đổi theo domain của bạn)
        verification_url = f"http://localhost:5000/api/v1/auth/verify-email?token={token}"
        
        body = f"""
        <html>
            <body>
                <h2>Xin chào {username}!</h2>
                <p>Cảm ơn bạn đã đăng ký tài khoản tại hệ thống của chúng tôi.</p>
                <p>Vui lòng click vào link bên dưới để xác nhận email của bạn:</p>
                <p><a href="{verification_url}">Xác nhận email</a></p>
                <p>Hoặc copy link sau vào trình duyệt:</p>
                <p>{verification_url}</p>
                <p><strong>Lưu ý:</strong> Link này sẽ hết hạn sau 15 phút.</p>
                <br>
                <p>Nếu bạn không thực hiện đăng ký này, vui lòng bỏ qua email này.</p>
                <p>Trân trọng,<br>Đội ngũ hỗ trợ</p>
            </body>
        </html>
        """
        
        return self._send_email(to_email, subject, body)
    
    def send_password_reset_email(self, to_email, username, token):
        """
        Gửi email reset mật khẩu
        
        Args:
            to_email: Email người nhận
            username: Tên người dùng
            token: Token reset password
        """
        subject = "Yêu cầu đặt lại mật khẩu"
        
        # URL reset password (Frontend sẽ xử lý)
        reset_url = f"http://localhost:3000/reset-password?token={token}"
        
        body = f"""
        <html>
            <body>
                <h2>Xin chào {username}!</h2>
                <p>Chúng tôi nhận được yêu cầu đặt lại mật khẩu cho tài khoản của bạn.</p>
                <p>Vui lòng click vào link bên dưới để đặt lại mật khẩu:</p>
                <p><a href="{reset_url}">Đặt lại mật khẩu</a></p>
                <p>Hoặc copy link sau vào trình duyệt:</p>
                <p>{reset_url}</p>
                <p><strong>Lưu ý:</strong> Link này sẽ hết hạn sau 15 phút.</p>
                <br>
                <p>Nếu bạn không thực hiện yêu cầu này, vui lòng bỏ qua email này và mật khẩu của bạn sẽ không thay đổi.</p>
                <p>Trân trọng,<br>Đội ngũ hỗ trợ</p>
            </body>
        </html>
        """
        
        return self._send_email(to_email, subject, body)
    
    def _send_email(self, to_email, subject, body):
        """
        Hàm nội bộ gửi email
        
        Returns:
            tuple: (success: bool, message: str)
        """
        # Mock mode cho development
        if self.mock_mode:
            print("=" * 60)
            print("📧 EMAIL MOCK MODE")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"Body:\n{body}")
            print("=" * 60)
            return True, "Email sent (mock mode)"
        
        # Production mode - Gửi email thật
        try:
            # Tạo message
            message = MIMEMultipart('alternative')
            message['From'] = self.from_email
            message['To'] = to_email
            message['Subject'] = subject
            
            # Attach HTML body
            html_part = MIMEText(body, 'html')
            message.attach(html_part)
            
            # Kết nối SMTP và gửi
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()  # Bảo mật TLS
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(message)
            
            return True, "Email sent successfully"
            
        except Exception as e:
            print(f"❌ Email sending failed: {str(e)}")
            return False, f"Failed to send email: {str(e)}"
    
    def send_welcome_email(self, to_email, username):
        """
        Gửi email chào mừng sau khi xác nhận thành công
        """
        subject = "Chào mừng bạn đến với hệ thống!"
        
        body = f"""
        <html>
            <body>
                <h2>Xin chào {username}!</h2>
                <p>Tài khoản của bạn đã được kích hoạt thành công.</p>
                <p>Bạn có thể đăng nhập vào hệ thống và bắt đầu sử dụng các tính năng.</p>
                <p>Nếu có bất kỳ thắc mắc nào, vui lòng liên hệ với chúng tôi.</p>
                <p>Trân trọng,<br>Đội ngũ hỗ trợ</p>
            </body>
        </html>
        """
        
        return self._send_email(to_email, subject, body)
