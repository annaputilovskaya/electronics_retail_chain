from django.db import models

from suppliers.models import Organization


class Product(models.Model):
    """
    Модель продукта организации.
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="products", verbose_name='Организация')
    name = models.CharField(max_length=100, verbose_name="Название продукта")
    model = models.CharField(max_length=255, verbose_name="Модель продукта")
    launched_at = models.DateField(verbose_name="Дата выхода продукта на рынок")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} ({self.model})"
