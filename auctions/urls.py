from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("closed_listings", views.closed, name="closed"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.view_category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("ARWatchlist/<int:key>/<str:title>", views.ARWatchlist, name="ARWatchlist"),
    path("listing/<str:title>", views.add_comment_or_bid, name="add_comment_or_bid"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<str:title>", views.view_listing, name="listing"),
]
