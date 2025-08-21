from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class ProfileForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=150)

    class Meta:
        model = Profile
        fields = ['photo']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = self.instance.user
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
            profile.save()
        return profile
