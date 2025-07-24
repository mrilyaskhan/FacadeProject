# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile
import re

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a strong password'
        }),
        label="Password",
        help_text="Password must contain: uppercase, lowercase, number, and special character"
    )

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }),
        }
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            errors = []
            
            # Check for at least one uppercase letter
            if not re.search(r'[A-Z]', password):
                errors.append("At least one uppercase letter (A-Z)")
                
            # Check for at least one lowercase letter
            if not re.search(r'[a-z]', password):
                errors.append("At least one lowercase letter (a-z)")
                
            # Check for at least one number
            if not re.search(r'[0-9]', password):
                errors.append("At least one number (0-9)")
                
            # Check for at least one special character
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                errors.append("At least one special character (!@#$ etc.)")
            
            if errors:
                raise ValidationError(
                    "Password must contain: " + ", ".join(errors))
        
        return password