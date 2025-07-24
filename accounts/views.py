from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, UserCreateForm
from django.contrib.auth.models import User
from django.contrib import messages

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile
    })

def add_user_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'This username is already taken. Please choose another.')
            else:
                try:
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    messages.success(request, "User created successfully!")
                    return redirect('dashboard')
                except Exception as e:
                    messages.error(request, f"Error creating user: {str(e)}")
    else:
        form = UserCreateForm()
    
    return render(request, 'accounts/add_user.html', {'form': form})