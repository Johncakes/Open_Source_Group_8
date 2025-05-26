from django.shortcuts import render, get_object_or_404
from movie.models.movie import Movie

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'feature_detail_page.html', {'movie': movie})

def movie_search(request):
    query = request.GET.get('q', '')
    field = request.GET.get('field', 'title')
    sort = request.GET.get('sort', 'latest')
    #results = []
    results = Movie.objects.all()  # 기본: 전체에서 시작

    if query:
        if field == 'title':
            results = Movie.objects.filter(title__icontains=query)
        elif field == 'original_title':
            results = Movie.objects.filter(original_title__icontains=query)
    if sort == 'latest':
        results = Movie.objects.order_by('-release_date')
    elif sort == 'popular':
        results = Movie.objects.order_by('-popularity')

    return render(request, 'search.html', {
        'query': query,
        'field': field,
        'sort': sort,
        'results': results
    })