from django.urls import path

from . import views


app_name = "profiles"
urlpatterns = [
    path("<int:pk>/", views.profile, name="detail"),
    path("<int:pk>/update/", views.ProfileUpdateView.as_view(), name="update"),

    path("<int:user_pk>/follow/", views.follow, name="follow"),
    path("<int:user_pk>/unfollow/", views.unfollow, name="unfollow"),
]

