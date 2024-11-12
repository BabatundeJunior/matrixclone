from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout


# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in new users automatically after signup
            return redirect('core:home')
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, 'authentication/signup.html', context)


def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('core:home')  # (To redirect to home after login)
            else:
                # Optional: Handle invalid login
                form.add_error(None, "Invalid username or password")

    context = {'form': form}
    return render(request, 'authentication/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('core:home')  # Redirect to home page after logout
