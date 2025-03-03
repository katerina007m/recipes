from django.urls import path
from .views import (
    ShopIndexView,
    GroupListView,
    ProductListView,
    orders_list,
    create_product,
    ProductDetailView,
)


app_name = "shopapp"

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupListView.as_view(), name="group_list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_details"),
    path("products/create/", create_product, name="products_create"),
    path("orders/", orders_list, name="orders_list"),
]