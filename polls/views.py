from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db import IntegrityError

from .models import Poll, Choice, Vote
from .forms import PollForm, ChoiceForm


def poll_list(request):
    page = int(request.GET["page"]) if "page" in request.GET else 1
    polls = Poll.objects.all().order_by('-date_added')
    paginator = Paginator(polls, 4)
    is_paginated = paginator.num_pages > 1
    page_obj = paginator.page(page)
    object_list = page_obj.object_list

    context = {
        "is_paginated": is_paginated,
        "page_obj": page_obj,
        "object_list": object_list,
    }
    return render(request, "polls/poll_list.html", context)


@login_required()
def poll_subscribed_list(request):
    page = int(request.GET["page"]) if "page" in request.GET else 1
    followed_users = request.user.follower.values('followed')
    selected_choices = request.user.vote_set.values('choice')
    answered_polls = Choice.objects.filter(id__in=selected_choices).values('question')

    queryset1 = Poll.objects.filter(author__in=followed_users).order_by('-date_added')
    queryset2 = Poll.objects.filter(id__in=answered_polls)
    queryset = queryset1 | queryset2

    paginator = Paginator(queryset, 4)
    is_paginated = paginator.num_pages > 1
    page_obj = paginator.page(page)
    object_list = page_obj.object_list

    context = {
        "is_paginated": is_paginated,
        "page_obj": page_obj,
        "object_list": object_list,
    }
    return render(request, "polls/poll_list.html", context)


def poll_detail(request, pk):
    _object = get_object_or_404(Poll, id=pk)
    if request.user.is_authenticated:
        selections = Vote.objects.filter(user=request.user, choice__in=_object.choice_set.all()).values_list('choice', flat=True)
    else:
        selections = []
    context = {
        "object": _object,
        "selections": selections,
    }
    return render(request, "polls/poll_detail.html", context)


@login_required()
def poll_create(request):
    form = PollForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid:
            form.instance.author = request.user
            form.save()
            return redirect(reverse("polls:poll_detail", kwargs={"pk": form.instance.id}))

    context = {
        "form": form,
        "redirect": reverse("polls:poll_create"),
        "action": "Create",
    }
    return render(request, "polls/poll_form.html", context)


@login_required()
def poll_update(request, pk):
    poll = get_object_or_404(Poll, id=pk)
    if request.user != poll.author:
        return HttpResponseForbidden()
    
    form = PollForm(request.POST or None, instance=poll)

    if request.method == "POST":
        if form.is_valid:
            form.instance.author = request.user
            form.save()
            return redirect(reverse("polls:poll_detail", kwargs={"pk": form.instance.id}))

    context = {
        "form": form,
        "redirect": reverse("polls:poll_update", kwargs={"pk": pk}),
        "action": "Update",
    }
    return render(request, "polls/poll_form.html", context)


@login_required()
def poll_delete(request, pk):
    poll = get_object_or_404(Poll, id=pk)
    if request.user != poll.author:
        return HttpResponseForbidden()

    if request.method == "POST":
        poll.delete()
        return redirect(reverse("polls:poll_list"))

    context = {
        "object": poll,
    }
    return render(request, "polls/poll_delete_confirm.html", context)


@login_required()
def choice_create(request, poll_pk):
    poll = get_object_or_404(Poll, id=poll_pk)
    if request.user != poll.author:
        return HttpResponseForbidden()

    form = ChoiceForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid:
            form.instance.question = poll
            form.save()
            return redirect(reverse("polls:poll_detail", kwargs={"pk": poll.id}))

    context = {
        "form": form,
        "poll": poll,
        "redirect": reverse("polls:choice_create", kwargs={"poll_pk": poll.id}),
        "action": "Create",
    }
    return render(request, "polls/choice_form.html", context)


@login_required()
def choice_update(request, poll_pk, choice_pk):
    poll = get_object_or_404(Poll, id=poll_pk)
    if request.user != poll.author:
        return HttpResponseForbidden()

    choice = get_object_or_404(Choice, id=choice_pk, question__id=poll_pk)
    form = ChoiceForm(request.POST or None, instance=choice)

    if request.method == "POST":
        if form.is_valid:
            form.instance.question = choice.question
            form.save()
            return redirect(reverse("polls:poll_detail", kwargs={"pk": form.instance.question.id}))

    context = {
        "form": form,
        "poll": choice.question,
        "redirect": reverse("polls:choice_update", kwargs={"poll_pk": choice.question.id, "choice_pk": choice.id}),
        "action": "Update",
    }
    return render(request, "polls/choice_form.html", context)


@login_required()
def choice_delete(request, poll_pk, choice_pk):
    poll = get_object_or_404(Poll, id=poll_pk)
    if request.user != poll.author:
        return HttpResponseForbidden()

    choice = get_object_or_404(Choice, id=choice_pk, question__id=poll_pk)

    if request.method == "POST":
        choice.delete()
        return redirect(reverse("polls:poll_detail", kwargs={"pk": poll_pk}))

    context = {
        "object": choice,
    }
    return render(request, "polls/choice_delete_confirm.html", context)


@login_required()
def vote_update(request):
    choice_id = int(request.POST.get("flexRadioDefault"))
    user = request.user
    choice = get_object_or_404(Choice, id=choice_id)
    question = choice.question
    Vote.objects.filter(user=user, choice__in=question.choice_set.all()).delete()
    try:
        Vote.objects.create(user=user, choice=choice)
    except IntegrityError:
        pass
    return redirect(reverse("polls:poll_detail", kwargs={"pk": choice.question.pk}))