from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
import os

# Đăng ký font Roboto
def register_roboto_fonts():
    # Đường dẫn đến thư mục font Roboto
    roboto_dir = os.path.join(settings.STATIC_ROOT, "fonts", "Roboto", "static")
    
    # Đăng ký các biến thể font
    pdfmetrics.registerFont(TTFont("Roboto-Regular", os.path.join(roboto_dir, "Roboto-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Roboto-Bold", os.path.join(roboto_dir, "Roboto-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Roboto-Italic", os.path.join(roboto_dir, "Roboto-Italic.ttf")))



# Gọi hàm đăng ký font khi ứng dụng khởi động
register_roboto_fonts()



def generate_certificate(user, result):
    # Tạo buffer trong bộ nhớ
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Sử dụng font Roboto
    c.setFont("Roboto-Bold", 20)
    c.drawString(100, 750, "CHỨNG CHỈ HOÀN THÀNH KHÓA HỌC")  # Tiêu đề in đậm

    c.setFont("Roboto-Regular", 16)
    c.drawCentredString(300, 650, f"Họ và Tên: {user.get_full_name()}")
    c.drawCentredString(300, 620, f"Khóa học: {result.exam.title}")
    c.drawCentredString(300, 590, f"Ngày cấp: {result.created_at.strftime('%d/%m/%Y')}")
    c.drawCentredString(300, 560, f"Điểm đạt được: {result.score}%")
    
    c.save()
    buffer.seek(0)
    return buffer