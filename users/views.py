from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.permissions import IsActiveUser
from users.serializers import UserSerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Контроллер списка пользователей."
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Контроллер создания пользователя."
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Контроллер изменения пользователя."
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Контроллер изменения пользователя."
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Контроллер удаления пользователя."
    ),
)
class UserViewSet(ModelViewSet):
    """
    Контроллер пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        """
        Получает права доступа для разных действий.
        """
        if self.action in ["create"]:
            self.permission_classes = (AllowAny,)
        elif self.action in ["update", "destroy"]:
            self.permission_classes = (IsAdminUser,)
        elif self.action in ["retrieve", "list"]:
            self.permission_classes = (IsActiveUser,)
        return super().get_permissions()
