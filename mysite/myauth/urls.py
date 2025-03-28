from django.urls import path

from .views import (
    MyLoginView,
    AboutMeView,
    RegisterView,
    logout_view,
)

app_name = "myauth"

urlpatterns = [
    path(
        "login/",
        MyLoginView.as_view(
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", logout_view, name="logout"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("register/", RegisterView.as_view(), name="register"),
]
