from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_list, name='manage_exams'),
     path("add", views.add_exam, name="add_exam"),
    path("edit/<int:exam_id>", views.edit_exam, name="edit_exam"),
    path("delete/<int:exam_id>", views.delete_exam, name="delete_exam"),
]
