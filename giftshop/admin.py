from django.contrib import admin

# Register your models here.
from .models import Ecard, GiftShop


class GiftShopAdmin(admin.ModelAdmin):
    # inlines = [
    #     GiftShop,
    # ]
    list_display = [
        'id', 'title', 'product_price', 'discount_active', 'discount_price'
    ]
    list_display_links = ('title', )


class EcardAdmin(admin.ModelAdmin):
    # inlines = [
    #     GiftShop,
    # ]
    list_display = [
        'id', 'title', 'product_price', 'discount_active', 'discount_price'
    ]
    list_display_links = ('title', )


admin.site.register(GiftShop, GiftShopAdmin)
admin.site.register(Ecard, EcardAdmin)
