from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
def future_temp(request):
    return render(request, 'future_temp.html')
