from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.serializers import ModelSerializer

from products.serializers import ProductSerializer
from suppliers.models import Contacts, Organization
from suppliers.validators import SupplierValidator, DebtValidator


class ContactsSerializer(ModelSerializer):
    """
    Сериализатор контактов организации.
    """
    class Meta:
        model = Contacts
        read_only_fields = ('organization',)
        exclude = ('id',)


class OrganizationSerializer(WritableNestedModelSerializer):
    """
    Сериализатор организации.
    """
    contacts = ContactsSerializer()
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = "__all__"
        read_only_fields = ('hierarchy_level', 'debt', 'created_at')
        validators = [
            SupplierValidator(),
            DebtValidator(),
        ]
