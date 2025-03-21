from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from .models import Certificate
from results.models import Result
from .utils import generate_certificate

@login_required
def certificate_list(request):
    certificates = Certificate.objects.all()
    return render(request, 'certificate_list.html', {'certificates': certificates})
@login_required
def issue_certificate(request, result_id):
    result = get_object_or_404(Result, id=result_id, user=request.user)

    # Kiểm tra xem chứng chỉ đã tồn tại chưa
    certificate, created = Certificate.objects.get_or_create(user=request.user, result=result)
    
    if created or not certificate.pdf_file:
        pdf_path = generate_certificate(request.user, result)
        certificate.pdf_file = pdf_path.replace(settings.MEDIA_ROOT + "/", "")
        certificate.save()

    return render(request, "certificate_detail.html", {"certificate": certificate})

@login_required
def download_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id, user=request.user)
    file_path = os.path.join(settings.MEDIA_ROOT, certificate.pdf_file)
    return FileResponse(open(file_path, "rb"), content_type="application/pdf", as_attachment=True)
# This view function generates a certificate for a user based on a completed exam result. If the certificate does not exist or the PDF file is missing, it generates a new certificate and saves it to the media folder. The user can then view or download the certificate.