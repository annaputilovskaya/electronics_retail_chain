from django.db import models

NULLABLE = {"blank": True, "null": True}


class Organization(models.Model):
    """
    Модель организации.
    """

    ORGANIZATION_TYPE_CHOICES = [
        ("individual", "Индивидуальный предприниматель"),
        ("retail", "Розничная сеть"),
        ("factory", "Завод"),
    ]

    name = models.CharField(max_length=255, verbose_name="Название организации")
    organization_type = models.CharField(
        max_length=50, choices=ORGANIZATION_TYPE_CHOICES, verbose_name="Тип организации"
    )

    supplier = models.ForeignKey(
        "self", **NULLABLE, on_delete=models.SET_NULL, verbose_name="Поставщик"
    )
    hierarchy_level = models.SmallIntegerField(
        **NULLABLE, default=0, verbose_name="Уровень иерархии"
    )

    debt = models.DecimalField(
        max_digits=16, decimal_places=2, default=0, verbose_name="Задолженность"
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return f"{self.name}"


class Contacts(models.Model):
    """
    Модель контактов организации.
    """

    organization = models.OneToOneField(
        Organization,
        related_name="contacts",
        on_delete=models.CASCADE,
        verbose_name="Организация",
    )
    email = models.EmailField(**NULLABLE, verbose_name="Электронная почта")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house = models.CharField(max_length=50, verbose_name="Номер дома")

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return (
            f"{self.email}; {self.country}, {self.city}, {self.street}, {self.house}."
        )
