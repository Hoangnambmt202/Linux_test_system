from django.urls import path
from . import views

urlpatterns = [
    path("", views.manage_results, name='manage_results'),
    path("submit/<int:exam_id>/", views.submit_exam, name="submit_exam"),
    path("view_result/<int:result_id>/", views.view_result_user, name="view_result_user"),
]
