from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def user_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    actual_decorator = user_passes_test(
        lambda u: not u.is_doctor,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def doc_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    actual_decorator = user_passes_test(
        lambda u: u.is_doctor,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
