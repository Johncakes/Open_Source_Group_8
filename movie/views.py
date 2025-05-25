from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from movie.models import Review
from movie.models.movie import Movie

def index(request):
    movie = Movie.objects.all()
    return render(request, 'index.html', {'movie': movie})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, "feature_detail_page.html", {"movie": movie})


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
