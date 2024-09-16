from rest_framework.viewsets import ModelViewSet

from products.models import Product
from products.serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    """
    Контроллер продукта.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
