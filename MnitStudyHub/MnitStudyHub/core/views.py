from django.shortcuts import render, get_object_or_404
from .models import Category, Resource
# Create your views here.
def BrowseResources(request):

    categories = Category.objects.all()
    return render(request, 'BrowseResources.html', {'categories': categories})

def category_resources(request, slug):

    category = get_object_or_404(Category, slug=slug)
    resources = Resource.objects.filter(category=category)
    return render(request, 'category_resources.html', {'category': category, 'resources': resources})
