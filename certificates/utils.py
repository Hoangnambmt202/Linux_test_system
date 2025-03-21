from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from django.conf import settings

def generate_certificate(user, result):
    file_path = os.path.join(settings.MEDIA_ROOT, "certificates", f"certificate_{user.id}_{result.id}.pdf")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    c = canvas.Canvas(file_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(300, 700, "CHỨNG CHỈ HOÀN THÀNH KHÓA HỌC")

    c.setFont("Helvetica", 16)
    c.drawCentredString(300, 650, f"Họ và Tên: {user.get_full_name()}")
    c.drawCentredString(300, 620, f"Khóa học: {result.exam.title}")
    c.drawCentredString(300, 590, f"Ngày cấp: {result.created_at.strftime('%d/%m/%Y')}")
    c.drawCentredString(300, 560, f"Điểm đạt được: {result.score}%")

    c.save()
    return file_path
# This function generates a PDF certificate for a user who has completed a course. The certificate includes the user's name, the course title, the issue date, and the score achieved. The PDF is saved to the "certificates" directory in the media folder.