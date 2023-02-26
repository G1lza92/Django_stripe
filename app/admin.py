from django.contrib import admin

from .models import Item, ItemsInOrder, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """ Shows the Item model in the admin panel"""
    list_display = (
        'pk',
        'name',
        'description',
        'price',
        # 'currency',
    )
    list_filter = (
        'name',
    )


class ItemsInOrderInline(admin.TabularInline):
    model = ItemsInOrder
    extra = 0
    readonly_fields = (
        'item_name',
    )

    def item_name(self, instance):
        return instance.item.name


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Shows the Order model in the admin panel"""
    list_display = (
        'pk',
        'user',
        'get_items',
        'total_price',
        'paid',
    )
    list_filter = (
        'user',
        'paid',
    )
    inlines = (ItemsInOrderInline,)
