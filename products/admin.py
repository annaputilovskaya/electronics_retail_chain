from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "model", "launched_at")
    list_filter = ("id", "name", "model", "launched_at")
