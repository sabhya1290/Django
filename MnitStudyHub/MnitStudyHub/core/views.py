from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Resource, Subject
from collections import defaultdict
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import os
from django.conf import settings
from django.http import FileResponse
from django.http import Http404
from django.views.decorators.http import require_POST

# Create your views here.
def BrowseResources(request):

    categories = Category.objects.all()
    return render(request, 'BrowseResources.html', {'categories': categories})

from .models import Bookmark

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

    user = request.user if request.user.is_authenticated else None
    bookmarks = set()
    if user:
        bookmarks = set(Bookmark.objects.filter(user=user, pdf_id__in=resources.values_list('id', flat=True)).values_list('pdf_id', flat=True))

    for res in resources:
        res.is_bookmarked = res.id in bookmarks
        grouped_data[res.get_department_display()][res.subject].append(res)
    grouped_data = {dept: dict(subjects) for dept, subjects in grouped_data.items()}

    return render(request, 'subjects.html', {'branch': branch, 'resources': grouped_data})


def architecture_and_planning(request):
    categories = ArchitectureAndPlanning.objects.all()
    return render(request, 'achitecturePlanning.html', {'categories': categories})

def architecture_and_planning_resources(request, slug):
    branch = get_object_or_404(ArchitectureAndPlanning, slug=slug)
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

    user = request.user if request.user.is_authenticated else None
    bookmarks = set()
    if user:
        bookmarks = set(Bookmark.objects.filter(user=user, pdf_id__in=resources.values_list('id', flat=True)).values_list('pdf_id', flat=True))

    for res in resources:
        res.is_bookmarked = res.id in bookmarks
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


@require_POST
@login_required
def toggle_bookmark(request, pdf_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=403)
    try:
        resource = Resource.objects.get(id=pdf_id)
    except Resource.DoesNotExist:
        return JsonResponse({'error': 'Resource not found'}, status=404)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, pdf=resource)
    if not created:
        bookmark.delete()
        return JsonResponse({'bookmarked': False})
    return JsonResponse({'bookmarked': True})

@login_required
def bookmark(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request, 'bookmark.html', {'bookmarks': bookmarks})

@login_required
def delete_bookmark(request, pdf_id):
    bookmark = get_object_or_404(Bookmark, pdf_id=pdf_id, user=request.user)
    if request.method == "POST":
        bookmark.delete()
        return redirect('bookmark')
    return redirect('bookmark')

def pdf_view(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    print(f"DEBUG: Looking for PDF at: {file_path}")
    if not os.path.exists(file_path):
        print("DEBUG: File does not exist!")
        raise Http404("PDF not found")
    try:
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['X-Frame-Options'] = 'ALLOWALL'
        return response
    except Exception as e:
        print(f"DEBUG: Error opening file: {e}")
        raise

