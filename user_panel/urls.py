from django.urls import path, include
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path("profile/exam-history/", views.exam_history_view, name="exam_history"),
    path("profile/certificates/", views.certificates_view, name="certificates"),
    path("profile/support/", views.support_view, name="support"),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('exam/', include('exams.urls')),
    path('result/', include('results.urls')),
    path("support", views.support_view, name="support"),
    path("notifications", views.notifications_view, name="notifications"),

]
