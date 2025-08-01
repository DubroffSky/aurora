from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomAuthenticationForm

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
            return redirect('home')
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
