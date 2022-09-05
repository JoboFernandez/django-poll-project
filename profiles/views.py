from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.core.paginator import Paginator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from .models import Profile, UserFollow


def profile(request, pk):
    page = int(request.GET["page"]) if "page" in request.GET else 1
    model_object = get_object_or_404(Profile, user=pk)
    paginator = Paginator(model_object.user.poll_set.all().order_by('-date_added'), 4)
    is_paginated = paginator.num_pages > 1
    page_obj = paginator.page(page)
    object_list = page_obj.object_list
    delete_redirect = "/posts/user"

    context = {
        "object": model_object,
        "is_paginated": is_paginated,
        "page_obj": page_obj,
        "object_list": object_list,
        "delete_redirect": delete_redirect,
    }

    return render(request, "profiles/profile_detail.html", context)


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "profiles/profile_form.html"
    model = Profile
    fields = ['image', 'location', 'gender']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user

    def get_success_url(self):
        return reverse("profiles:detail", kwargs={"pk": self.get_object().user.id})


@login_required()
def follow(request, user_pk):
    follower = request.user
    followed = User.objects.get(id=user_pk)
    try:
        UserFollow.objects.create(follower=follower, followed=followed)
    except IntegrityError:
        pass
    return redirect(request.META.get("HTTP_REFERER"))


@login_required()
def unfollow(request, user_pk):
    follower = request.user
    followed = User.objects.get(id=user_pk)
    _follow = UserFollow.objects.get(follower=follower, followed=followed)
    _follow.delete()
    return redirect(request.META.get("HTTP_REFERER"))