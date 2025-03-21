from django.urls import path
from . import views

urlpatterns = [
    path("manage", views.manage_questions, name="manage_questions"),
    path("add", views.add_question, name="add_question"),
    path("edit/<int:question_id>/", views.edit_question, name="edit_question"),
    path("delete/<int:question_id>/", views.delete_question, name="delete_question"),
]
