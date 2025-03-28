from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Certificate
from results.models import Result
from .utils import generate_certificate
from django.http import HttpResponse

@login_required
def certificate_list(request):
    certificates = Certificate.objects.all()
    return render(request, 'certificate_list.html', {'certificates': certificates})

def issue_certificate(user, result_id):
    result = get_object_or_404(Result, id=result_id, user=user)
    
    # Chỉ tạo bản ghi Certificate (không liên quan đến file)
    certificate, created = Certificate.objects.get_or_create(
        user=user,
        result=result
    )
    return certificate

@login_required
def download_certificate(request, certificate_id):
    # Kiểm tra quyền truy cập
    certificate = get_object_or_404(Certificate, id=certificate_id, user=request.user)
    
    # Tạo PDF trong bộ nhớ
    try:
        pdf_buffer = generate_certificate(request.user, certificate.result)
        response = HttpResponse(pdf_buffer.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="certificate_{certificate_id}.pdf"'
        return response
    except Exception as e:
        return HttpResponse(f"Lỗi tạo chứng chỉ: {str(e)}", status=500)
# This view function generates a certificate for a user based on a completed exam result. If the certificate does not exist or the PDF file is missing, it generates a new certificate and saves it to the media folder. The user can then view or download the certificate.