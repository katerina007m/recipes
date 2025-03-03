from django.urls import path
from .views import (
    ShopIndexView,
    GroupListView,
    ProductListView,
    OrderListView,
    create_product,
    ProductDetailView,
    OrderDetailView,
)


app_name = "shopapp"

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupListView.as_view(), name="group_list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_details"),
    path("products/create/", create_product, name="products_create"),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
]