from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from account.decorators import anonymous_required
from account.forms import CustomAuthenticationForm, CustomSignupForm


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
