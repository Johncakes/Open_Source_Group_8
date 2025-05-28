from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from movie.models import Review
from movie.models.movie import Movie
from django.db.models import Avg


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    average_rating = movie.reviews.aggregate(avg=Avg('rating'))['avg']
    return render(request, 'feature_detail_page.html', {
        'movie': movie,
        'average_rating': average_rating
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
