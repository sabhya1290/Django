from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Resource, Subject
from collections import defaultdict
from django.db.models import Q
from django.contrib.auth.decorators import login_required
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
            Q(subject__name__icontains=query) |
            Q(department__icontains=query)
        )

    grouped_data = defaultdict(lambda: defaultdict(list))

    for res in resources:
        grouped_data[res.get_department_display()][res.subject].append(res)
    grouped_data = {dept: dict(subjects) for dept, subjects in grouped_data.items()}

    return render(request, 'subjects.html', {'branch': branch, 'resources': grouped_data})

@login_required
def upload_pdf(request):
    departments = Resource.DEPARTMENT_CHOICES
    subjects = Subject.objects.all()
    if request.method == "POST":
        title = request.POST['title']
        file = request.FILES['file']
        subject_id = request.POST['subject']
        year = request.POST['year']
        department = request.POST['department']
        user = request.user
        try:
            subject = Subject.objects.get(id=subject_id)
            Resource.objects.create(
                title=title,
                file=file,
                subject=subject,
                year=year,
                department=department,
                user=user
            )
            return render(request, 'upload.html', {
                'subjects': subjects,
                'departments': departments,
                'success': 'Notes uploaded successfully!'
            })
        except Exception as e:
            return render(request, 'upload.html', {
                'subjects': subjects,
                'departments': departments,
                'error': str(e)
            })
    return render(request, 'upload.html', {'subjects': subjects, 'departments': departments})


@login_required
def YourNotes(request):
    notes = Resource.objects.filter(user=request.user)
    return render(request, 'YourNotes.html', {'notes': notes})

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Resource, id=note_id, user=request.user)
    if request.method == "POST":
        note.delete()
        return redirect('your_notes')
    return redirect('your_notes')







