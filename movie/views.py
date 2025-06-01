from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from movie.models import Review
from movie.models.movie import Movie
from django.db.models import Avg

def index(request):
    movie = Movie.objects.all()
    popular_movie = movie.order_by('-popularity')[:30]
    random_movie = movie.order_by('?')[:30]
    return render(request, 'index.html', {'movie': movie, 'popular_movie': popular_movie, 'random_movie': random_movie})

def get_star_list(rating):
    full = int(rating)
    half = 1 if rating - full >= 0.25 and rating - full < 0.75 else 0
    empty = 5 - full - half
    return ['full'] * full + ['half'] * half + ['empty'] * empty

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    average_rating = movie.reviews.aggregate(avg=Avg('rating'))['avg']
    star_list = get_star_list(average_rating or 0)
    return render(request, 'feature_detail_page.html', {
        'movie': movie,
        'average_rating': average_rating,
        'star_list': star_list
    })


@require_POST
def create_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    review = Review.anonymous_review(
        movie=movie,
        content=request.POST.get("content", "").strip(),
        rating=request.POST.get("rating"),
    )

    try:
        review.full_clean()
        review.save()
    except ValueError:
        return redirect("movie_detail", movie_id=movie.id)

    return redirect("movie_detail", movie_id=movie.id)
