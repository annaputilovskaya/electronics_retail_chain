from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet

from products.models import Product
from products.paginators import ProductPaginator
from products.serializers import ProductSerializer
from users.permissions import IsActiveUser


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Контроллер списка продуктов с постраничным выводом."
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(operation_description="Контроллер создания продукта."),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(operation_description="Контроллер изменения продукта."),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(operation_description="Контроллер изменения продукта."),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="Контроллер удаления продукта."),
)
class ProductViewSet(ModelViewSet):
    """
    Контроллер продукта.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsActiveUser,)
    pagination_class = ProductPaginator
