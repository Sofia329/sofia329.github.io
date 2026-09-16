
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("newposts", views.newpost, name="newpost"),
    path("allposts", views.allposts, name="allposts"),
    path("allposts/<int:post_id>", views.editpost, name="editpost"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("myposts", views.myposts, name="myposts")
   
]
