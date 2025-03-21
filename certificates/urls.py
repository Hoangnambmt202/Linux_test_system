from django.urls import path
from . import views

urlpatterns = [
    path('', views.certificate_list, name='certificate_list'),
    path("issue/<int:result_id>/", views.issue_certificate, name="issue_certificate"),
    path("download/<int:certificate_id>/", views.download_certificate, name="download_certificate"),
]
# This URL configuration includes two paths: one for issuing a certificate and one for downloading a certificate. The issue_certificate view generates a certificate for a user based on a completed exam result, while the download_certificate view allows the user to download the certificate as a PDF file.