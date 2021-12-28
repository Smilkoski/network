from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import (
    DetailView,
    ListView,
)
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin

from .models import User, Post, Follower


class ListAppendView(MultipleObjectMixin,
                     MultipleObjectTemplateResponseMixin,
                     ModelFormMixin,
                     ProcessFormView):
    """ A View that displays a list of objects and a form to create a new object.
    The View processes this form. """
    template_name = 'network/index.html'
    fields = ['title', 'content']
    allow_empty = True
    ordering = '-date_posted'
    model = Post

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object_list=self.object_list, form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        title = request.POST['title']
        content = request.POST['content']
        p = Post(author=request.user, title=title, content=content)
        p.save()
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list, form=form)
        return render(request, 'network/index.html', context)

    def form_invalid(self, form):
        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(object_list=self.object_list, form=form))


class UserDetailView(DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = {}
        signed_user = User.objects.get(pk=self.request.user.id)
        context['singed_user'] = signed_user
        visited_user = User.objects.get(pk=kwargs['object'].id)
        context['visited_user'] = visited_user

        if Follower.objects.filter(follower_id=signed_user, following_id=visited_user).count() > 0:
            context['follows'] = True
        else:
            context['follows'] = False

        context['followers'] = Follower.objects.filter(following_id=visited_user).count()
        context['following'] = Follower.objects.filter(follower_id=visited_user).count()

        context['posts'] = Post.objects.filter(author=visited_user).order_by('-date_posted')

        context['not_same_user'] = not (signed_user.id == visited_user.id)

        return context


class FollowingListView(ListView):
    model = Post
    context_object_name = 'object_list'
    template_name = 'network/following_users.html'

    def get_queryset(self):
        following_users = Follower.objects.filter(follower_id=self.request.user).select_related('following_id')
        following_users = [f.following_id.id for f in following_users]
        posts = []
        for i in following_users:
            posts += list(Post.objects.filter(author_id=i).all())

        return posts


def follow(request, pk1, pk2, *args, **kwargs):
    singed_user = User.objects.get(id=pk1)
    user_to_follow = User.objects.get(id=pk2)

    f = Follower(follower_id=singed_user, following_id=user_to_follow)
    f.save()

    return redirect(f"/detail/{user_to_follow.pk}")


def unfollow(request, pk1, pk2, *args, **kwargs):
    singed_user = User.objects.get(id=pk1)
    user_to_unfollow = User.objects.get(id=pk2)

    Follower.objects.filter(follower_id=singed_user, following_id=user_to_unfollow).delete()

    return redirect(f"/detail/{user_to_unfollow.pk}")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
