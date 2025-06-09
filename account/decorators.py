from django.contrib.auth.decorators import user_passes_test


def anonymous_required(view_func):
    return user_passes_test(
        lambda u: not u.is_authenticated,
        login_url="index",
        redirect_field_name=None,
    )(view_func)
