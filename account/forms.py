from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class CustomSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username"]
        labels = {
            "username": "아이디",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].label = "비밀번호"
        self.fields["password2"].label = "비밀번호 확인"

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "아이디"

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
