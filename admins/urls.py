from django.urls import path, include
from . import views

urlpatterns = [
    path("login/", views.admin_login, name="admin_login"),
    path('logout/', views.logout_view, name='logout'),
    path("", views.admin_dashboard, name="admin_dashboard"),
    path('users/manage', views.manage_users, name='manage_users'),
    path('manage-users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('manage-users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('exams/', include('exams.urls')),
    path('questions/', include('questions.urls')),
    path('results/', include('results.urls')),
    path("certificates/", include("certificates.urls")),
    
]
