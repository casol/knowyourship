from django.contrib import admin
from .models import ShipList, ShipDetails


class ShipListAdmin(admin.ModelAdmin):
    list_display = ('id', 'ship', 'country', 'region', 'city', 'from_country',
                    'year', 'ship_class', 'ship_type', 'remarks')
    list_filter = ('country', 'from_country')
    search_fields = list_display

admin.site.register(ShipList, ShipListAdmin)
admin.site.register(ShipDetails)
