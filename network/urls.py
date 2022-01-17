from django.urls import path

from .views import (
    ListAppendView,
    login_view,
    logout_view,
    register,
    UserListView,
    follow,
    unfollow,
    FollowingListView,
    PostDetailView,
    post,
    likes,
)

urlpatterns = [
    path("", ListAppendView.as_view(), name="index"),
    path("detail/<int:pk>/", UserListView.as_view(), name="user-detail"),
    path("post_detail/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("follow/<int:pk1>/<int:pk2>/", follow, name="follow"),
    path("unfollow/<int:pk1>/<int:pk2>/", unfollow, name="unfollow"),
    path("following/", FollowingListView.as_view(), name="following"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register, name="register"),
    # API Routes
    path("post/<int:post_id>", post, name="get_post"),
    path("likes/<int:post_id>", likes, name="get_likes"),
]
