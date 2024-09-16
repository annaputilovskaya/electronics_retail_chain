from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from suppliers.models import Organization
from suppliers.serializers import OrganizationSerializer
from users.permissions import IsActiveUser


# class ContactsViewSet(ModelViewSet):
#     """
#     Контроллер контактов организации.
#     """
#     queryset = Contacts.objects.all()
#     serializer_class = ContactsSerializer


class OrganizationViewSet(ModelViewSet):
    """
    Контроллер создания новой организации.
    """
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    permission_classes = (IsActiveUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("contacts__country",)

    def perform_create(self, serializer):
        """
        Устанавливает уровень иерархии организации в системе поставок
        при создании организации.
        """
        organization = serializer.save()
        if organization.organization_type == 'factory':
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
        if organization.organization_type == 'factory':
            organization.hierarchy_level = 0
        elif organization.supplier:
            supplier_id = organization.supplier.id
            supplier = Organization.objects.get(id=supplier_id)
            organization.hierarchy_level = supplier.hierarchy_level + 1
        else:
            organization.hierarchy_level = 1
        organization.save()
