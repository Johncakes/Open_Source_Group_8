
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q

from movie.models import Review

from movie.models.movie import Movie
from django.db.models import Avg

def index(request):
    movie = Movie.objects.all()
    popular_movie = movie.order_by('-popularity')[:30]
    random_movie = movie.order_by('?')[:30]
    return render(request, 'index.html', {'movie': movie, 'popular_movie': popular_movie, 'random_movie': random_movie})


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

def movie_search(request):
    query = request.GET.get('q', '')

    sort = request.GET.get('sort', 'latest')
    results = Movie.objects.all()  # 기본: 전체에서 시작

    if query:
        results = results.filter(
            Q(title__icontains=query) | Q(original_title__icontains=query)
        )
    if sort == 'latest':
        results = results.order_by('-release_date')
    elif sort == 'popular':
        results = results.order_by('-popularity')

    page_size = int(request.GET.get('size', 20))
    paginator = Paginator(results, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    current = page_obj.number
    total = paginator.num_pages

    start = max(current - 5, 1)
    end = min(current + 4, total)
    page_range = range(start, end + 1)

    return render(request, 'search.html', {
        'query': query,
        'sort': sort,
        'page_size': page_size,
        'page_obj': page_obj,
        'results': page_obj.object_list,
        'page_range': page_range,
        'total_pages': total,
    })

