from rest_framework.serializers import ValidationError


class SupplierValidator:
    """
    Валидатор поставщика.
    """
    def __call__(self, attrs):
        supplier = attrs.get("supplier")
        organization_type = attrs.get("organization_type")
        if supplier and organization_type == "factory":
            if supplier.organization_type != "factory":
                raise ValidationError("Поставщиком завода может быть только другой завод.")


class DebtValidator:
    """
    Валидатор задолженности.
    """
    def __call__(self, attrs):
        debt = attrs.get("debt")
        if debt and debt < 0:
            raise ValidationError("Задолженность не может быть отрицательной.")
