from django.urls        import path
from .                  import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("pizza/", views.pizza, name="pizza"),
    path("subs/", views.subs, name="subs"),
    path("pasta/", views.pasta, name="pasta"),
    path("salad/", views.salad, name="salad"),
    path("dinner/", views.dinner, name="dinner"),
    path("cart/", views.cart, name="cart"),
    path("error/", views.error, name="error")
]
