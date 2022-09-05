from django.urls import path

from . import views


app_name = "polls"
urlpatterns = [
    path("", views.poll_list, name="poll_list"),
    path("subscribed/", views.poll_subscribed_list, name="poll_subscribed_list"),
    path("<int:pk>/", views.poll_detail, name="poll_detail"),
    path("<int:pk>/update/", views.poll_update, name="poll_update"),
    path("<int:pk>/delete/", views.poll_delete, name="poll_delete"),
    path("create/", views.poll_create, name="poll_create"),

    path("<int:poll_pk>/choices/create/", views.choice_create, name="choice_create"),
    path("<int:poll_pk>/choices/<int:choice_pk>/update/", views.choice_update, name="choice_update"),
    path("<int:poll_pk>/choices/<int:choice_pk>/delete/", views.choice_delete, name="choice_delete"),

    path("vote_update/", views.vote_update, name="vote_update"),
]

