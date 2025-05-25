from django.shortcuts import render, get_object_or_404
from movie.models.movie import Movie

def index(request):
    movie = Movie.objects.all()
    return render(request, 'index.html', {'movie': movie})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'feature_detail_page.html', {'movie': movie})

