from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.cache import cache_page

from .views import (
    ShopIndexView,
    GroupListView,
    OrderListView,
    ProductCreateView,
    # create_order,
    ProductDetailsView,
    ProductListView,
    OrderDetailsView,
    ProductUpdateView,
    ProductDeleteView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    ProductsDataExportView,
    OrdersDataExportView,
    ProductViewSet,
    OrderViewSet,
    LatestProductFeed,
    UserOrdersListView,
    UserOrdersExportView,
)


app_name = 'shopapp'

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupListView.as_view(), name="groups_list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/export/", ProductsDataExportView.as_view(), name="products-export"),
    path("orders/", OrderListView.as_view(), name="orders_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    # path("orders/create/", create_order, name="order_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_delete"),
    path("orders/<int:pk>/", OrderDetailsView.as_view(), name="order_details"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/export/", OrdersDataExportView.as_view(), name="orders-export"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("api/", include(routers.urls)),
    path("products/latest/feed/", LatestProductFeed(), name="product_feed"),
    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name="users_orders"),
    path("users/<int:user_id>/orders/export/", UserOrdersExportView.as_view(), name="users_orders_export"),
]
