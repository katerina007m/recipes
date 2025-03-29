from django.urls import path

from myauth.views import MyLoginView, RegisterView, logout_view
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("recipe/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("recipe/add/", views.recipe_add, name="recipe_add"),
    path("login/", MyLoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", logout_view, name="logout"),
    path("recipe/delete/<int:pk>/", views.recipe_delete, name="recipe_delete"),
    path("recipe/edit/<int:pk>/", views.recipe_edit, name="recipe_edit"),
    path(
        "recipe/api/rec/<str:name>/",
        views.api_get_recipe_pk_by_name,
        name="api_get_recipe_pk_by_name",
    ),
    path(
        "recipe/api/cat/<str:name>/",
        views.api_get_category_pk_by_name,
        name="api_get_category_pk_by_name",
    ),
]
