from rest_framework.serializers import ModelSerializer

from products.models import Product


class ProductSerializer(ModelSerializer):
    """
    Сериализатор продукта.
    """
    class Meta:
        model = Product
        fields = "__all__"
