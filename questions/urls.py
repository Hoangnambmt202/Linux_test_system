from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.manage_questions, name="manage_questions"),
    path("add", views.add_question, name="add_question"),
    path("detail/<int:question_id>/", views.question_detail, name="question_detail"),
    path("edit/<int:question_id>/", views.edit_question, name="edit_question"),
    path("delete/<int:question_id>/", views.delete_question, name="delete_question"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
