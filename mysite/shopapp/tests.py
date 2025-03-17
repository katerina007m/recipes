from string import ascii_letters
from random import choices
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Product
from shopapp.utils import add_two_numbers


# Create your tests here.
class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        response = self.client.post(
            reverse('shopapp:product_create'),

            {
                'name': self.product_name,
                'price': "123.45",
                'description': "A good table",
                'discount': "10",
            },
            **{'HTTP_USER_AGENT': 'Mozilla/5.0'}
        )
        self.assertRedirects(response, reverse('shopapp:products_list'))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )


class ProductDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем общий экземпляр продукта для всех тестов
        cls.product = Product.objects.create(name="Best Product")

    @classmethod
    def tearDownClass(cls):
        # Удаляем продукт после всех тестов
        cls.product.delete()
        super().tearDownClass()

    def test_get_product(self):
        # Выполняем GET-запрос с заголовком HTTP_USER_AGENT
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk}),
            **{'HTTP_USER_AGENT': 'Mozilla/5.0'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Best Product")

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk}),
            **{'HTTP_USER_AGENT': 'Mozilla/5.0'}
        )
        self.assertContains(response, self.product.name)
