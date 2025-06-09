from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from movie.models import Review
from movie.models.movie import Genre, Movie


def index(request):
    movie = Movie.objects.all()
    popular_movie = movie.order_by("-popularity")[:30]
    random_movie = movie.order_by("?")[:30]
    reviews = Review.objects.select_related("movie").order_by("-created_at")[:10]

    recommended_movies = None
    if request.user.is_authenticated:
        top_genres = Genre.objects.top_reviewed_by_user(request.user)
        recommended_movies = Movie.objects.recommended_by_user(
            user=request.user, genres=top_genres, limit=15
        )

    return render(
        request,
        "index.html",
        {
            "movie": movie,
            "popular_movie": popular_movie,
            "random_movie": random_movie,
            "reviews": reviews,
            "recommended_movies" : recommended_movies,
        },
    )


def get_star_list(rating):
    full = int(rating)
    half = 1 if rating - full >= 0.25 and rating - full < 0.75 else 0
    empty = 5 - full - half
    return ["full"] * full + ["half"] * half + ["empty"] * empty


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    average_rating = movie.reviews.aggregate(avg=Avg("rating"))["avg"]
    star_list = get_star_list(average_rating or 0)
    return render(
        request,
        "movie_detail.html",
        {"movie": movie, "average_rating": average_rating, "star_list": star_list},
    )


@require_POST
def create_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    user = request.user

    if user.is_authenticated and Review.objects.filter(movie=movie, user=user).exists():
        messages.warning(request, "이미 이 영화에 리뷰를 작성하셨습니다.")
        return redirect("movie_detail", movie_id=movie.id)

    review = Review.generate_anonymous_review(
        movie=movie,
        user=request.user if request.user.is_authenticated else None,
        content=request.POST.get("content", "").strip(),
        rating=float(request.POST.get("rating")),
    )

    try:
        review.full_clean()
        review.save()
    except ValueError:
        return redirect("movie_detail", movie_id=movie.id)

    return redirect("movie_detail", movie_id=movie.id)


def movie_search(request):
    # GET 요청에서 검색어(query), 장르 선택(selected_genre), 정렬 방식(sort) 값을 받아옴
    query = request.GET.get("q", "")
    selected_genre = request.GET.get("genre", "")
    sort = request.GET.get("sort", "latest")
    # Movie 모델에서 모든 영화 데이터를 불러옴
    results = Movie.objects.all()
    # Genre 모델에서 모든 장르 목록을 가져옴
    genres = Genre.objects.all()

    # 검색어제목(title) 또는 원제(original_title)인 경우
    if query:
        results = results.filter(Q(title__icontains=query) | Q(original_title__icontains=query))
    # 정렬 조건 적용: 최신순 또는 인기순
    if sort == "latest":
        results = results.order_by("-release_date")
    elif sort == "popular":
        results = results.order_by("-popularity")
    # 선택된 장르에 속한 영화로 필터링
    if selected_genre:
        results = results.filter(genres__id=selected_genre)

    # 페이지 사이즈 설정 (기본값 20)
    page_size = int(request.GET.get("size", 20))
    paginator = Paginator(results, page_size)
    # 현재 페이지 번호 가져오기
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # 페이지네이션 범위 계산
    current = page_obj.number
    total = paginator.num_pages
    start = max(current - 2, 1)
    end = min(current + 2, total)
    page_range = range(start, end + 1)

    # 템플릿 렌더링: 검색 결과 및 관련 정보들 넘겨줌
    return render(
        request,
        "search.html",
        {
            "query": query,
            "sort": sort,
            "page_size": page_size,
            "page_obj": page_obj,
            "results": page_obj.object_list,
            "page_range": page_range,
            "total_pages": total,
            "selected_genre": selected_genre,
            "genres": genres,
        },
    )
