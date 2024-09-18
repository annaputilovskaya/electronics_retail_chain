from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product
from suppliers.models import Contacts, Organization
from users.models import User


class ProductTestCase(APITestCase):
    """
    Тестирование модели продукта.
    """

    def setUp(self):
        """
        Создание пользователя, организации, контактов и продуктов
        для тестирования.
        """

        self.user1 = User.objects.create(email="user1@example.com")
        self.organization = Organization.objects.create(
            name="Test Organization",
            organization_type="individual",
        )
        self.contacts = Contacts.objects.create(
            country="Test Country",
            city="Test City",
            street="Test Street",
            house="123",
            organization=self.organization,
        )
        self.product = Product.objects.create(
            name="Test Product",
            model=100,
            launched_at="2022-01-01",
            organization=self.organization,
        )
        self.product2 = Product.objects.create(
            name="Test Product",
            model=100,
            launched_at="2022-01-01",
            organization=self.organization,
        )
        self.client.force_authenticate(user=self.user1)

    def test_str_product(self):
        """
        Тестирование строчного представления продукта.
        """
        product = Product.objects.get(pk=self.product.pk)
        self.assertEqual(str(product), f"{self.product.name} ({self.product.model})")

    def test_product_create(self):
        """
        Тестирование создания нового продукта.
        """
        url = reverse("products:products-list")
        data = [
            {
                "name": "Test Product 2",
                "model": 200,
                "launched_at": "2022-02-01",
                "organization": self.organization.pk,
            },
            {
                "name": "Test Product 3",
                "model": 200,
                "launched_at": "2122-02-01",
                "organization": self.organization.pk,
            },
        ]
        # Тестируем корректное создание продукта
        response = self.client.post(url, data=data[0])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.get(name="Test Product 2"))

        # Тестируем создание продукта с некорректной датой
        response = self.client.post(url, data=data[1])
        message = response.json()["non_field_errors"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            message,
            ["Дата выхода продукта на рынок не может быть позднее текущей даты."],
        )

    def test_product_update(self):
        """
        Тестирование изменения существующего продукта.
        """
        url = reverse("products:products-detail", args=(self.product.pk,))
        data = {
            "name": "Updated Test Product",
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Product.objects.get(pk=self.product.pk).name, "Updated Test Product"
        )

    def test_product_delete(self):
        """
        Тестирование удаления существующего продукта.
        """
        url = reverse("products:products-detail", args=(self.product.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_product_retrieve(self):
        """
        Тестирование получения продукта по ID.
        """
        url = reverse("products:products-detail", args=(self.product.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Test Product")

    def test_product_list(self):
        """
        Тестирование получения списка всех продуктов.
        """
        url = reverse("products:products-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 2)
