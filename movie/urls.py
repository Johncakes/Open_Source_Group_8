from django.urls import path

from movie import views
from movie.views import index

urlpatterns = [
    path("", index, name="index"),
    path("movies/<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("movies/<int:movie_id>/reviews/", views.create_review, name="create_review"),
    path("search/", views.movie_search, name="movie_search"),
]
