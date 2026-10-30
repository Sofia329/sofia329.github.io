from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist",views.watchlist, name="watchlist"),
    path("<int:listpage>", views.listpage, name="listpage"),
    path("mylisting", views.mylisting, name="mylisting"),
    path("category", views.category, name="category"),
    path("amend/<int:listingID>", views.amend, name="amend_listing")
]
