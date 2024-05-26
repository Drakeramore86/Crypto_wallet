from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import LoginForm



@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'profile.html', {'profile': profile})


def loginUser(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        # Debug print
        print(f"Attempting to log in with email: {email}, password: {password}")

        # Assuming the username is the email for authentication
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # Debug print
            print(f'Logged in successfully as {user.username}')
            return redirect('home')
        else:
            # Debug print
            print('Login failed')
            messages.error(request, 'Invalid login credentials. Please try again.')
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a Profile object for the newly registered user
            Profile.objects.create(user=user)

            login(request, user)
            print('Registration successful. Welcome to our site!')
            messages.success(request, 'Registration successful. Welcome to our site!')
            return redirect('home')
        else:
            print(form.errors)  # Add this to see form errors in the terminal
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    print('You logged out successfully')
    messages.success(request, 'You logged out successfully')
    return redirect('home')