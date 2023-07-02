from string import ascii_letters
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from random import choices

from shopapp.models import Product


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
