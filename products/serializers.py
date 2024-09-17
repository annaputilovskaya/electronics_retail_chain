from rest_framework.serializers import ModelSerializer

from products.models import Product
from products.validators import DateValidator


class ProductSerializer(ModelSerializer):
    """
    Сериализатор продукта.
    """

    class Meta:
        model = Product
        fields = "__all__"
        validators = [
            DateValidator(),
        ]
