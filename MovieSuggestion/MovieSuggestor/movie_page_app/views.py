from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Movies
from django.shortcuts import get_object_or_404


# Create your views here.

@login_required
def moviepage(request):
    movies = Movies.objects.all().order_by('released_year')
    return render(request,'movies_page.html', {'movies': movies})

@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movies, pk=movie_id)
    return render(request, 'movie_detail.html', {'movie': movie})