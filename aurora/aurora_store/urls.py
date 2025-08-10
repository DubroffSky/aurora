from django.urls import path
from . import views

app_name = 'aurora_store'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # TaskFlow URLs
    path('tasks/', views.tasks_list, name='tasks_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/events/', views.calendar_view, name='calendar_events'),
    
    # Project Management URLs (Admin only)
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/invite/', views.invite_user, name='invite_user'),
    path('projects/<int:project_id>/remove-member/<int:user_id>/', views.remove_member, name='remove_member'),
] 