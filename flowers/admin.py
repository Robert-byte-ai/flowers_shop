from django.contrib import admin

from .models import Seller, Customer, Ad, Feedback, HiddenAds, Purchase


class SellerAdmin(admin.ModelAdmin):
    list_display = ("pk", "user",)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("pk", "user",)


class AdAdmin(admin.ModelAdmin):
    list_display = ('pk', 'flower', 'seller')


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content_object')


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("pk", "ad",)


admin.site.register(Seller, SellerAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(HiddenAds, AdAdmin)
admin.site.register(Purchase, PurchaseAdmin)
