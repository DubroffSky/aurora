from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Task, Project
from django.db import models

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email == 'admin@admin.admin':
            return email
        return email
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Required. 8 characters or more. Letters, digits and @/./+/-/_ only.'
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters and cannot be entirely numeric.'
        self.fields['password2'].help_text = 'Enter the same password as above, for verification.'

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )


# TaskFlow Forms
class ProjectForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Project
        fields = ['title', 'description', 'status', 'members']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project title'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter project description (max 50 words)',
                'maxlength': 500,
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        word_count = len(description.split())
        if word_count > 50:
            raise forms.ValidationError('Description must be 50 words or fewer.')
        return description


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 'priority', 'status', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter task description'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }   
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filter projects to show only owned by the user or where the user is a member
            self.fields['project'].queryset = Project.objects.filter(
                models.Q(owner=user) | models.Q(members=user)
            ).distinct()

            instance = kwargs.get('instance', None)
            project = None
            if instance:
                project = getattr(instance, 'project', None)
            else:
                # If the user is not the assigned user, filter the assigned_to field
                if not project:
                    project_id = self.data.get('project') or self.initial.get('project')
                    if project_id:
                        try:
                            project = Project.objects.get(pk=project_id)
                        except Project.DoesNotExist:
                            project = None
                if project:
                    members = project.members.all()
                    users = User.objects.filter(pk=project.owner.pk) | members
                    self.fields['assigned_to'].queryset = users.distinct()
                # else:
                #     self.fields['assigned_to'].queryset = User.objects.none()