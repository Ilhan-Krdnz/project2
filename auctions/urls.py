from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/comment",views.comment, name="comment"),
    #path("<int:pk>/comment_remove",views.comment_remove, name="comment_delete"),
    path('<int:pk>/bid',views.bidding, name="bidding"),
    path("create",views.make_listing, name='make_listing'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]