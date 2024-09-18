from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from suppliers.models import Organization
from suppliers.paginators import OrganizationPaginator
from suppliers.serializers import OrganizationSerializer
from users.permissions import IsActiveUser


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Контроллер списка организаций с постраничным выводом."
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Контроллер создания организации."
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Контроллер изменения организации."
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Контроллер изменения организации."
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Контроллер удаления организации."
    ),
)
class OrganizationViewSet(ModelViewSet):
    """
    Контроллер организации.
    """

    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    permission_classes = (IsActiveUser,)
    pagination_class = OrganizationPaginator
    filter_backends = (filters.SearchFilter,)
    search_fields = ("contacts__country",)

    def perform_create(self, serializer):
        """
        Устанавливает уровень иерархии организации в системе поставок
        при создании организации.
        """
        organization = serializer.save()
        if organization.organization_type == "factory":
            organization.hierarchy_level = 0
        elif organization.supplier:
            supplier_id = organization.supplier.id
            supplier = Organization.objects.get(id=supplier_id)
            organization.hierarchy_level = supplier.hierarchy_level + 1
        else:
            organization.hierarchy_level = 1
        organization.save()

    def perform_update(self, serializer):
        """
        Устанавливает уровень иерархии организации в системе поставок
        при изменении информации организации.
        """
        organization = serializer.save()
        if organization.organization_type == "factory":
            organization.hierarchy_level = 0
        elif organization.supplier:
            supplier_id = organization.supplier.id
            supplier = Organization.objects.get(id=supplier_id)
            organization.hierarchy_level = supplier.hierarchy_level + 1
        else:
            organization.hierarchy_level = 1
        organization.save()
