from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.models import StudentProfile

def home(request):
    return render(request, 'home.html')
def future_temp(request):
    return render(request, 'future_temp.html')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('BrowseResources')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def custom_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        year = request.POST['year']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password1)
        StudentProfile.objects.create(user=user, year=year)
        login(request, user)
        return redirect('BrowseResources')
    return render(request, 'register.html')

def custom_logout(request):
    logout(request)
    return redirect('home')