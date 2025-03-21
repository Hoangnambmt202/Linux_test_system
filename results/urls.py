from django.urls import path
from .views import submit_exam, view_result, manage_results

urlpatterns = [
    path('manage', manage_results, name='manage_results'),
    path("submit/<int:exam_id>/", submit_exam, name="submit_exam"),
    path("view/<int:result_id>/", view_result, name="view_result"),
]
