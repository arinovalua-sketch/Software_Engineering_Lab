from django.contrib import admin
from .models import Item, Claim

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'item_type', 'category', 'date_created')
    list_filter = ('item_type', 'category')
    search_fields = ('title', 'description', 'location')


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'status')
    list_filter = ('status',)
admin.site.site_header = "Lost & Found Admin"
admin.site.site_title = "Lost & Found"
admin.site.index_title = "Dashboard"

