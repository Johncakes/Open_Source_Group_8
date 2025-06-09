from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from account.decorators import anonymous_required
from account.forms import CustomAuthenticationForm, CustomSignupForm
from movie.models import Genre, Movie, Review


@anonymous_required
def signup(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomSignupForm()

    return render(request, "account/signup.html", {"form": form})


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "account/login.html"


class CustomLogoutView(LogoutView): ...


@login_required
def profile(request):
    reviews = Review.objects.find_by_user(request.user)
    average_rating = reviews.average_rating()
    top_genres = Genre.objects.top_reviewed_by_user(request.user)
    recommended_movies = Movie.objects.recommended_by_user(
        user=request.user, genres=top_genres, limit=12
    )

    return render(
        request,
        "account/profile.html",
        {
            "reviews": reviews,
            "average_rating": average_rating,
            "top_genres": top_genres,
            "recommended_movies": recommended_movies,
        },
    )
