from django.shortcuts import render, get_object_or_404
from movie.models.movie import Movie

def index(request):
    movie = Movie.objects.all()
    popular_movie = movie.order_by('-popularity')[:30]
    random_movie = movie.order_by('?')[:30]
    return render(request, 'index.html', {'movie': movie, 'popular_movie': popular_movie, 'random_movie': random_movie})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'feature_detail_page.html', {'movie': movie})

