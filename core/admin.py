from django.contrib import admin
from .models import ListOfMuseumShips


class ListOfMuseumShipAdmin(admin.ModelAdmin):
    list_display = ('ship', 'country', 'region', 'city', 'from_country',
                    'year', 'ship_class', 'ship_type', 'remarks')
    list_filter = ('country', 'from_country')
    search_fields = list_display

admin.site.register(ListOfMuseumShips, ListOfMuseumShipAdmin)
