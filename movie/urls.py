from django.urls import path
from movie.views import index
from movie import views

urlpatterns = [
    path('', index, name='index'),
    path("movies/<int:movie_id>/", views.movie_detail, name='movie_detail'),
]
