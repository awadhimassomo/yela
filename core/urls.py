from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('accounts/register/', views.student_register, name='student_register'),
    path('accounts/login/', views.student_login, name='student_login'),
    path('accounts/logout/', views.student_logout, name='student_logout'),
    path('programs/apply/', views.program_apply, name='program_apply'),
]
