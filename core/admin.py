from django.contrib import admin
from .models import ShipList, ShipDetails, ShipCoordinates


class ShipDetailsInline(admin.TabularInline):
    """Edit models on the same page as a parent model(ShipList)."""
    model = ShipDetails


class ShipCoordinatesInline(admin.StackedInline):
    """Edit models on the same page as a parent model(ShipList)."""
    model = ShipCoordinates


class ShipListAdmin(admin.ModelAdmin):
    list_display = ('id', 'ship', 'country', 'region', 'city', 'from_country',
                    'year', 'ship_class', 'ship_type', 'remarks')
    list_filter = ('country', 'from_country')
    search_fields = list_display
    inlines = [
        ShipDetailsInline,
        ShipCoordinatesInline
    ]

admin.site.register(ShipList, ShipListAdmin)

