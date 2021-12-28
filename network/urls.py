from django.urls import path

from .views import (
    ListAppendView,
    login_view,
    logout_view,
    register,
    UserDetailView,
    follow,
    unfollow,
)

urlpatterns = [
    path("", ListAppendView.as_view(), name="index"),
    path("detail/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("follow/<int:pk1>/<int:pk2>/", follow, name="follow"),
    path("unfollow/<int:pk1>/<int:pk2>/", unfollow, name="unfollow"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register, name="register"),
]
