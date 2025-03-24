from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.exam_list, name='manage_exams'),
    path("add", views.add_exam, name="add_exam"),
    path("edit/<int:exam_id>", views.edit_exam, name="edit_exam"),
    path("delete/<int:exam_id>", views.delete_exam, name="delete_exam"),
    path('take/<int:exam_id>/', views.take_exam, name="take_exam"),
    path('results/', include('results.urls')),
]
