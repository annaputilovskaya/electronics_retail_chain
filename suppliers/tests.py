from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from suppliers.models import Organization, Contacts
from users.models import User


class OrganizationTestCase(APITestCase):
    """
    Тестирование модели организации.
    """
    def setUp(self):
        """
        Создание пользователя, организации и контактов
        для тестирования.
        """

        self.user1 = User.objects.create(email="user1@example.com")
        self.organization1 = Organization.objects.create(
            name='Test Organization 1',
            organization_type='factory',
            )
        self.organization2 = Organization.objects.create(
            name='Test Organization 2',
            organization_type='retail',
            supplier=self.organization1,
            )
        self.contacts1 = Contacts.objects.create(
            country='Test Country',
            city='Test City',
            street='Test Street',
            house='123',
            organization=self.organization1,
        )
        self.contacts2 = Contacts.objects.create(
            country='Test Country',
            city='Test City',
            street='Test Street',
            house='123',
            organization=self.organization2,
        )

        self.client.force_authenticate(user=self.user1)

    def test_str_organization(self):
        """
        Тестирование строчного представления организации.
        """
        organization = Organization.objects.get(pk=self.organization1.pk)
        self.assertEqual(str(organization), self.organization1.name)

    def test_organization_retrieve(self):
        """
        Тестирование получения информации об организации по ID.
        """
        url = reverse("suppliers:organization-detail", args=[self.organization1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.organization1.name)

    def test_organization_list(self):
        """
        Тестирование получения списка всех организаций.
        """
        url = reverse("suppliers:organization-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual((response.data["count"]), Organization.objects.count())

    def test_organization_delete(self):
        """
        Тестирование удаления организации по ID.
        """
        url = reverse("suppliers:organization-detail", args=[self.organization1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Organization.objects.all().count(), 1)

    def test_organization_update(self):
        """
        Тестирование изменения информации об организации.
        """
        url = reverse("suppliers:organization-detail", args=[self.organization1.pk])
        data = [
            {"name": "Organ"},
            {"debt": 100},
            ]

        # Тестируем корректное изменениие информации об организации.
        response = self.client.patch(url, data[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data[0]["name"])

        # Тестируем изменение долга организации.
        response = self.client.patch(url, data[1])
        self.assertNotEqual(response.data["debt"], data[1]["debt"])
