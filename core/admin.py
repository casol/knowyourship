from django.contrib import admin
from .models import ShipList, ShipDetails, ShipCoordinates, ShipImage, Comment


class ShipDetailsInline(admin.TabularInline):
    """Edit models on the same page as a parent model(ShipList)."""
    model = ShipDetails


class ShipCoordinatesInline(admin.StackedInline):
    """Edit models on the same page as a parent model(ShipList)."""
    model = ShipCoordinates


class ShipListAdmin(admin.ModelAdmin):
    list_display = ('ship', 'id', 'country', 'region', 'city', 'from_country',
                    'year', 'ship_class', 'ship_type', 'remarks', 'url')
    list_filter = ('country', 'from_country')
    prepopulated_fields = {'slug': ('ship',)}
    search_fields = list_display
    inlines = [
        ShipDetailsInline,
        ShipCoordinatesInline
    ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'ship', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.register(ShipList, ShipListAdmin)
admin.site.register(ShipImage)
admin.site.register(Comment, CommentAdmin)