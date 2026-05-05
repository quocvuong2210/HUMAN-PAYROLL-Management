"""
Email OTP Service - Gmail SMTP thật
Gửi OTP qua Gmail, không mock
"""
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class EmailOTPService:
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.smtp_from = os.getenv('SMTP_FROM', self.smtp_user)
        self.otp_expire_minutes = int(os.getenv('OTP_EXPIRE_MINUTES', 5))
        
        # Validate configuration
        if not self.smtp_user or not self.smtp_password:
            raise ValueError("SMTP_USER and SMTP_PASSWORD must be set in .env file")
    
    def generate_otp(self, length=6):
        """
        Generate random OTP code
        
        Args:
            length: Length of OTP (default 6)
        
        Returns:
            str: OTP code
        """
        return ''.join(random.choices(string.digits, k=length))
    
    def send_otp_email(self, to_email, otp_code, username=None):
        """
        Gửi OTP qua Gmail SMTP thật
        
        Args:
            to_email: Email người nhận
            otp_code: Mã OTP
            username: Tên người dùng (optional)
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Mã xác thực OTP - HR Payroll System'
            msg['From'] = self.smtp_from
            msg['To'] = to_email
            
            # HTML content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 20px;
                        overflow: hidden;
                        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 40px 20px;
                        text-align: center;
                        color: white;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 28px;
                        font-weight: 600;
                    }}
                    .content {{
                        padding: 40px 30px;
                    }}
                    .greeting {{
                        font-size: 18px;
                        color: #333;
                        margin-bottom: 20px;
                    }}
                    .otp-box {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 15px;
                        padding: 30px;
                        text-align: center;
                        margin: 30px 0;
                    }}
                    .otp-code {{
                        font-size: 48px;
                        font-weight: bold;
                        color: white;
                        letter-spacing: 10px;
                        font-family: 'Courier New', monospace;
                    }}
                    .otp-label {{
                        color: rgba(255,255,255,0.9);
                        font-size: 14px;
                        margin-top: 10px;
                    }}
                    .info {{
                        background: #f8f9fa;
                        border-left: 4px solid #667eea;
                        padding: 15px 20px;
                        margin: 20px 0;
                        border-radius: 5px;
                    }}
                    .info p {{
                        margin: 5px 0;
                        color: #555;
                        font-size: 14px;
                    }}
                    .warning {{
                        background: #fff3cd;
                        border-left: 4px solid #ffc107;
                        padding: 15px 20px;
                        margin: 20px 0;
                        border-radius: 5px;
                    }}
                    .warning p {{
                        margin: 5px 0;
                        color: #856404;
                        font-size: 14px;
                    }}
                    .footer {{
                        text-align: center;
                        padding: 20px;
                        color: #999;
                        font-size: 12px;
                        border-top: 1px solid #eee;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔐 HR Payroll System</h1>
                    </div>
                    <div class="content">
                        <div class="greeting">
                            Xin chào{' ' + username if username else ''},
                        </div>
                        <p style="color: #555; line-height: 1.6;">
                            Bạn đã yêu cầu mã OTP để xác thực tài khoản. 
                            Vui lòng sử dụng mã bên dưới để hoàn tất quá trình đăng ký:
                        </p>
                        
                        <div class="otp-box">
                            <div class="otp-code">{otp_code}</div>
                            <div class="otp-label">Mã xác thực OTP</div>
                        </div>
                        
                        <div class="info">
                            <p><strong>⏰ Thời gian hiệu lực:</strong> {self.otp_expire_minutes} phút</p>
                            <p><strong>🔒 Bảo mật:</strong> Mã OTP chỉ sử dụng được 1 lần</p>
                        </div>
                        
                        <div class="warning">
                            <p><strong>⚠️ Lưu ý bảo mật:</strong></p>
                            <p>• Không chia sẻ mã OTP này với bất kỳ ai</p>
                            <p>• Nếu bạn không yêu cầu mã này, vui lòng bỏ qua email</p>
                            <p>• Mã OTP sẽ hết hiệu lực sau {self.otp_expire_minutes} phút</p>
                        </div>
                        
                        <p style="color: #555; margin-top: 30px; font-size: 14px;">
                            Nếu bạn gặp vấn đề, vui lòng liên hệ bộ phận hỗ trợ.
                        </p>
                    </div>
                    <div class="footer">
                        <p>© 2026 HR Payroll System. All rights reserved.</p>
                        <p>Email này được gửi tự động, vui lòng không trả lời.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Connect to SMTP server and send
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()  # Enable TLS
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True, "OTP đã được gửi đến email của bạn"
            
        except smtplib.SMTPAuthenticationError:
            return False, "Lỗi xác thực email. Vui lòng kiểm tra cấu hình SMTP."
        except smtplib.SMTPException as e:
            return False, f"Lỗi gửi email: {str(e)}"
        except Exception as e:
            return False, f"Lỗi không xác định: {str(e)}"
    
    def send_welcome_email(self, to_email, username):
        """
        Gửi email chào mừng sau khi đăng ký thành công
        
        Args:
            to_email: Email người nhận
            username: Tên người dùng
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Chào mừng đến với HR Payroll System'
            msg['From'] = self.smtp_from
            msg['To'] = to_email
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 20px;
                        overflow: hidden;
                        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 40px 20px;
                        text-align: center;
                        color: white;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 32px;
                        font-weight: 600;
                    }}
                    .content {{
                        padding: 40px 30px;
                    }}
                    .welcome-text {{
                        font-size: 24px;
                        color: #333;
                        text-align: center;
                        margin-bottom: 20px;
                        font-weight: 600;
                    }}
                    .success-icon {{
                        text-align: center;
                        font-size: 80px;
                        margin: 20px 0;
                    }}
                    .footer {{
                        text-align: center;
                        padding: 20px;
                        color: #999;
                        font-size: 12px;
                        border-top: 1px solid #eee;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎉 Chào mừng!</h1>
                    </div>
                    <div class="content">
                        <div class="success-icon">✅</div>
                        <div class="welcome-text">Xin chào {username}!</div>
                        <p style="color: #555; line-height: 1.8; text-align: center;">
                            Tài khoản của bạn đã được tạo thành công.<br>
                            Bạn có thể đăng nhập và bắt đầu sử dụng hệ thống ngay bây giờ.
                        </p>
                    </div>
                    <div class="footer">
                        <p>© 2026 HR Payroll System. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True, "Email chào mừng đã được gửi"
            
        except Exception as e:
            # Don't fail registration if welcome email fails
            print(f"Warning: Failed to send welcome email: {str(e)}")
            return False, str(e)
