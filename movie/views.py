from django.shortcuts import render, get_object_or_404
from movie.models.movie import Movie
from django.db.models import Q  # 이거 추가

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'feature_detail_page.html', {'movie': movie})

def movie_search(request):
    query = request.GET.get('q', '')

    sort = request.GET.get('sort', 'latest')
    #results = []
    results = Movie.objects.all()  # 기본: 전체에서 시작

    if query:
        results = results.filter(
            Q(title__icontains=query) | Q(original_title__icontains=query)
        )
    if sort == 'latest':
        results = results.order_by('-release_date')
    elif sort == 'popular':
        results = results.order_by('-popularity')

    return render(request, 'search.html', {
        'query': query,

        'sort': sort,
        'results': results
    })