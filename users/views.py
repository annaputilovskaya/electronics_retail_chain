from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.permissions import IsActiveUser
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    Контроллер пользователей.
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
