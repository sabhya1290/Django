from django.shortcuts import render, get_object_or_404
from .models import Category, Resource
from collections import defaultdict
from django.db.models import Q

# Create your views here.
def BrowseResources(request):

    categories = Category.objects.all()
    return render(request, 'BrowseResources.html', {'categories': categories})

def category_resources(request, slug):

    branch = get_object_or_404(Category, slug=slug)
    query = request.GET.get('q', '')
    year = branch.year
    resources = Resource.objects.filter(year=year[0])


    if query:
        resources = resources.filter(
            Q(title__icontains=query) |
            Q(subject__icontains=query) |
            Q(department__icontains=query)
        )

    grouped_data = defaultdict(lambda: defaultdict(list))

    for res in resources:
        grouped_data[res.get_department_display()][res.subject].append(res)
    grouped_data = {dept: dict(subjects) for dept, subjects in grouped_data.items()}

    return render(request, 'subjects.html', {'branch': branch, 'resources': grouped_data})
