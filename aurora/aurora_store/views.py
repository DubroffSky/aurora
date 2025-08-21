from .profile_form import ProfileForm
from django.contrib.auth.decorators import login_required
# Profile settings view
@login_required
def profile_settings(request):
    # Ensure user has a profile
    profile, created = getattr(request.user, 'profile', None), False
    if profile is None:
        from .models import Profile
        profile = Profile.objects.create(user=request.user)
        created = True
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('aurora_store:profile')
    else:
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, 'aurora_store/profile_settings.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.utils import timezone
import json
from .forms import CustomUserCreationForm, CustomAuthenticationForm, TaskForm, ProjectForm
from .models import Task, Project
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def home(request):
    """Main page"""
    return render(request, 'aurora_store/home.html')

def register(request):
    """View for user registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('aurora_store:home')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'aurora_store/register.html', {'form': form})

def user_login(request):
    """View for user login"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('aurora_store:home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'aurora_store/login.html', {'form': form})

@login_required
def user_logout(request):
    """View for user logout"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('aurora_store:home')

@login_required
def profile(request):
    """User profile page"""
    return render(request, 'aurora_store/profile.html')


# TaskFlow Views
@login_required
def tasks_list(request):
    """User's tasks list"""
    tasks = Task.objects.filter(
        models.Q(assigned_to=request.user) |
        models.Q(project__owner=request.user)
    ).distinct().select_related('project', 'assigned_to', 'created_by')
    
    context = {
        'tasks': tasks,
        'status_choices': Task.STATUS_CHOICES,
        'priority_choices': Task.PRIORITY_CHOICES,
    }
    return render(request, 'aurora_store/tasks_list.html', context)


@login_required
def task_create(request):
    """Create a new task"""
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('aurora_store:tasks_list')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = TaskForm(user=request.user)
    
    return render(request, 'aurora_store/task_form.html', {'form': form, 'title': 'Create Task'})


@login_required
def task_edit(request, task_id):
    """Edit task"""
    task = get_object_or_404(Task, id=task_id)
    
    # Check access rights
    if not (request.user == task.created_by or 
            request.user == task.assigned_to or 
            request.user == task.project.owner or 
            request.user in task.project.members.all()):
        messages.error(request, 'You do not have permission to edit this task.')
        return redirect('aurora_store:tasks_list')
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('aurora_store:tasks_list')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = TaskForm(instance=task, user=request.user)
    
    return render(request, 'aurora_store/task_form.html', {'form': form, 'title': 'Edit Task'})


@login_required
def task_delete(request, task_id):
    """Delete task"""
    task = get_object_or_404(Task, id=task_id)
    
    # Check access rights
    if not (request.user == task.created_by or request.user == task.project.owner):
        messages.error(request, 'You do not have permission to delete this task.')
        return redirect('aurora_store:tasks_list')
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('aurora_store:tasks_list')
    
    return render(request, 'aurora_store/task_confirm_delete.html', {'task': task})


# @login_required

# Project Management Views (Admin only)
@login_required
def projects_list(request):
    """Список проектов (only for admins)"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to view projects.')
        return redirect('aurora_store:home')
    
    projects = Project.objects.all().select_related('owner').prefetch_related('members')
    
    context = {
        'projects': projects,
    }
    return render(request, 'aurora_store/projects_list.html', context)


@login_required
def project_create(request):
    """Create a new project (only for admins)"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to create projects.')
        return redirect('aurora_store:home')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()  # Save many-to-many fields
            messages.success(request, 'Project created successfully!')
            return redirect('aurora_store:projects_list')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ProjectForm()
    
    return render(request, 'aurora_store/project_form.html', {'form': form, 'title': 'Create Project'})


@login_required
def project_edit(request, project_id):
    """Edit project (only for admins)"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit projects.')
        return redirect('aurora_store:home')
    
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('aurora_store:projects_list')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'aurora_store/project_form.html', {'form': form, 'title': 'Edit Project'})


@login_required
def project_detail(request, project_id):
    """Detailed information about the project (only for admins)"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to view project details.')
        return redirect('aurora_store:home')
    
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project).select_related('assigned_to', 'created_by')
    
    context = {
        'project': project,
        'tasks': tasks,
    }
    return render(request, 'aurora_store/project_detail.html', context)


@login_required
def invite_user(request, project_id):
    """Invitation to the project by email (only for admins)"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to invite users.')
        return redirect('aurora_store:home')
    
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                # Check if a user with this email exists
                user = User.objects.get(email=email)
                
                # Add user to the project
                project.members.add(user)
                
                # Send email notification
                try:
                    send_mail(
                        subject=f'You have been invited to project: {project.title}',
                        message=f'''
                        Hello {user.username}!
                        
                        You have been invited to join the project "{project.title}".
                        
                        Project details:
                        - Title: {project.title}
                        - Description: {project.description or 'No description'}
                        - Owner: {project.owner.username}
                        
                        You can now view and work on tasks in this project.
                        
                        Best regards,
                        TaskFlow Team
                        ''',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=True,
                    )
                    messages.success(request, f'User {user.username} has been invited to the project!')
                except Exception as e:
                    messages.warning(request, f'User added to project, but email notification failed: {str(e)}')
                
            except User.DoesNotExist:
                messages.error(request, f'User with email {email} does not exist.')
            except Exception as e:
                messages.error(request, f'Error inviting user: {str(e)}')
        else:
            messages.error(request, 'Please provide a valid email address.')
    
    return redirect('aurora_store:project_detail', project_id=project_id)


@login_required
def remove_member(request, project_id, user_id):
    """Remove member from the project (only for admins)"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to remove members.')
        return redirect('aurora_store:home')
    
    project = get_object_or_404(Project, id=project_id)
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        project.members.remove(user)
        messages.success(request, f'User {user.username} has been removed from the project.')
    
    return redirect('aurora_store:project_detail', project_id=project_id)
