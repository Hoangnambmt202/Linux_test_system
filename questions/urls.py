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
    path('topics/', views.manage_topics, name='manage_topics'),
    path('topics/edit/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    path('topics/delete/<int:topic_id>/', views.delete_topic, name='delete_topic'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
