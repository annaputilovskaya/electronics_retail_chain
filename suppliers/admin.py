from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from suppliers.models import Organization


@admin.action(description="Обнуление задолженности перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    for organization in queryset:
        organization.debt = 0
        organization.save()


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "organization_type",
        "view_supplier_link",
        "debt",
        "view_contacts__city",
        "hierarchy_level",
    ]
    readonly_fields = ["debt", "hierarchy_level"]
    actions = [clear_debt]
    list_filter = [
        "contacts__city",
    ]

    def view_supplier_link(self, organization):
        """
        Представляет ссылку на поставщика.
        """
        supplier = organization.supplier
        if supplier:
            display_text = "<a href={}>{}</a>".format(
                reverse(
                    "admin:{}_{}_change".format(
                        organization._meta.app_label, organization._meta.model_name
                    ),
                    args=(supplier.pk,),
                ),
                supplier.name,
            )
            if display_text:
                return mark_safe(display_text)
            return "-"

    view_supplier_link.short_description = "Поставщики"

    def view_contacts__city(self, organization):
        """
        Представляет город из контактов организации.
        """
        contacts = organization.contacts
        return contacts.city

    view_contacts__city.short_description = "Город"
