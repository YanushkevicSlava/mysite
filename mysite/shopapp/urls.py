from django.urls import path
from .views import shop_index, groups_list, products_list, orders_lisr, \
    create_product


app_name = 'shopapp'

urlpatterns = [
    path("", shop_index, name="index"),
    path("groups/", groups_list, name="groups_list"),
    path("products/", products_list, name="products_list"),
    path("orders/", orders_lisr, name="orders_list"),
    path("products/create/", create_product, name="product_create"),

]
