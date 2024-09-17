from rest_framework.viewsets import ModelViewSet

from products.models import Product
from products.paginators import ProductPaginator
from products.serializers import ProductSerializer
from users.permissions import IsActiveUser


class ProductViewSet(ModelViewSet):
    """
    Контроллер продукта.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsActiveUser,)
    pagination_class = ProductPaginator
