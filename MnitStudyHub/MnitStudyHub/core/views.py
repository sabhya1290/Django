from django.shortcuts import render
from .models import Category
# Create your views here.
def BrowseResources(request):
    
    categories = Category.objects.all()
    return render(request, 'BrowseResources.html', {'categories': categories})
