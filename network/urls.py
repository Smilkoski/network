from django.urls import path

from .views import (
    ListAppendView,
    login_view,
    logout_view,
    register
)

urlpatterns = [
    path("", ListAppendView.as_view(), name="index"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register, name="register"),
]
