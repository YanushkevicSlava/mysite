from string import ascii_letters
from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse
from random import choices
from django.core import serializers
from shopapp.models import Product, Order


class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        url = reverse("shopapp:products_list")
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "A good table",
                "discount": "10"
            },
            HTTP_USER_AGENT='Mozilla/5.0',
        )
        self.assertRedirects(response, f'/myauth/login/?next={url}create%2F')
        self.assertFalse(
            Product.objects.filter(name=self.product_name).exists(),
        )


class ProductDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="Best Product")

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk}),
            HTTP_USER_AGENT='Mozilla/5.0',
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk}),
            HTTP_USER_AGENT='Mozilla/5.0',
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]

    def test_products(self):
        response = self.client.get(reverse("shopapp:products_list"), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertQuerysetEqual(
            qs=list(Product.objects.filter(archived=False).all()),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, "shopapp/products-list.html")


class OrderListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="sara_test", password="qwert")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_order_view(self):
        response = self.client.get(reverse("shopapp:orders_list"), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertContains(response, "Order")

    def test_order_view_no_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        "products-fixture.json"
    ]

    def test_get_products_view(self):
        response = self.client.get(reverse("shopapp:products-export"), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data
        )


class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username='Holmes-test', password='qwerty')
        permission_order = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission_order)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address='Baker street, 221b',
            promocode='SALE_123',
            user=self.user)

    def tearDown(self) -> None:
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(reverse(
            'shopapp:order_details',
            kwargs={'pk': self.order.pk}),
            HTTP_USER_AGENT='Mozilla/5.0',
        )
        received_data = response.context["order"].pk
        expected_data = self.order.pk
        self.assertEqual(received_data, expected_data)
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)


class OrdersExportViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="sara_test", password="qwert", is_staff="True")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    fixtures = [
        "orders-fixture.json"
    ]

    def test_get_orders_view(self):
        response = self.client.get(reverse("shopapp:orders-export"), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by("id").all()
        expected_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user": str(order.user),
                "products": serializers.serialize('json', order.products.all(),
                                                  use_natural_primary_keys=True,
                                                  fields="name"),
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(
            orders_data["orders"],
            expected_data
        )
