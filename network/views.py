import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    ListView,
    DetailView,
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
    paginate_by = 10

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


class UserListView(ListView):
    context_object_name = 'object_list'
    template_name = 'network/user_detail.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author=self.kwargs['pk']).order_by('-date_posted')

    def get_context_data(self, *args, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)

        signed_user = User.objects.get(pk=self.request.user.id)
        context['singed_user'] = signed_user
        visited_user = User.objects.get(pk=self.kwargs['pk'])
        context['visited_user'] = visited_user

        if Follower.objects.filter(follower_id=signed_user, following_id=visited_user).count() > 0:
            context['follows'] = True
        else:
            context['follows'] = False

        context['followers'] = Follower.objects.filter(following_id=visited_user).count()
        context['following'] = Follower.objects.filter(follower_id=visited_user).count()

        context['not_same_user'] = not (signed_user.id == visited_user.id)

        return context


class FollowingListView(ListView):
    model = Post
    context_object_name = 'object_list'
    template_name = 'network/following_users.html'
    paginate_by = 10

    def get_queryset(self):
        following_users = Follower.objects.filter(follower_id=self.request.user).select_related('following_id')
        following_users = [f.following_id.id for f in following_users]
        posts = []
        for i in following_users:
            posts += list(Post.objects.filter(author_id=i).all())

        return posts


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'object'


@csrf_exempt
@login_required
def post(request, post_id):
    # Query for requested post
    try:
        post = Post.objects.get(author=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("title") is not None and data.get("content") is not None:
            post.title = data["title"]
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)

    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


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
