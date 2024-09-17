from django.utils import timezone
from rest_framework.serializers import ValidationError


class DateValidator:
    """
    Валидатор даты выхода продукта на рынок.
    """
    def __call__(self, attrs):
        date = attrs.get("launched_at")
        if date > timezone.now().date():
            raise ValidationError("Дата выхода продукта на рынок не может быть позднее текущей даты.")
