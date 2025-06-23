from django.shortcuts import render
from .forms import  UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('movies_page')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form':form})
    
