from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm
from django.db import transaction, IntegrityError
from django import forms


@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    print(profile.name)  # Print profile data to ensure it's fetched correctly
    return render(request, 'profile.html', {'profile': profile})


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


def loginUser(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # Debug print
        print(f"Attempting to log in with username: {username}, password: {password}")

        user = authenticate(request, username=username, password=password)
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
        user_form = CustomUserCreationForm(request.POST)

        profile_data = request.POST.copy()
        for key in ['username', 'email', 'password1', 'password2', 'csrfmiddlewaretoken']:
            profile_data.pop(key, None)

        profile_form = ProfileForm(profile_data, request.FILES)

        print("User Form Data:", user_form.data)  # Debug print
        print("Profile Form Data:", profile_form.data)  # Debug print
        print("Profile Form FILES:", request.FILES)  # Debug print

        if user_form.is_valid() and profile_form.is_valid():
            print("Both forms are valid.")  # Debug print
            try:
                with transaction.atomic():
                    user = user_form.save()
                    print("User created:", user)  # Debug print

                    # Check if a profile already exists
                    profile, created = Profile.objects.get_or_create(user=user)
                    profile.name = profile_form.cleaned_data.get('name')
                    profile.last_name = profile_form.cleaned_data.get('last_name')
                    profile.short_intro = profile_form.cleaned_data.get('short_intro')
                    if 'account_photo' in request.FILES:
                        profile.account_photo = request.FILES['account_photo']
                    profile.save()

                    login(request, user)
                    print("User logged in:", user)  # Debug print
                    messages.success(request, 'Registration successful. Welcome to our site!')
                    return redirect('home')
            except IntegrityError as e:
                print("IntegrityError:", e)
                messages.error(request, 'There was an error creating your profile. Please try again.')
        else:
            print("User Form Errors:", user_form.errors)  # Debug print
            print("Profile Form Errors:", profile_form.errors)  # Debug print
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()

    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


def logout_view(request):
    logout(request)
    print('You logged out successfully')
    messages.success(request, 'You logged out successfully')
    return redirect('home')
