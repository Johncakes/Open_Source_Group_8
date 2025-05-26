from django.shortcuts import render, get_object_or_404
from movie.models.movie import Movie
from django.db.models import Avg

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    average_rating = movie.reviews.aggregate(avg=Avg('rating'))['avg']
    return render(request, 'feature_detail_page.html', {
        'movie': movie,
        'average_rating': average_rating
    })
