from django.contrib import admin
from .models import UserProfile, Order, PaymentProof, OrderFieldConfig,Offer,Banner
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ('full_name', 'user', 'contact', 'alt_contact')
    search_fields = ('full_name', 'contact', 'user__email')

@admin.register(OrderFieldConfig)
class OrderFieldConfigAdmin(admin.ModelAdmin):
    list_display  = ('label', 'field_key', 'field_type', 'is_enabled', 'is_required', 'order')
    list_editable = ('is_enabled', 'is_required', 'order')   # edit directly from list!
    list_filter   = ('is_enabled', 'field_type')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'service', 'status', 'user', 'created_at')
    list_filter   = ('status', 'service')
    search_fields = ('name', 'user__email', 'room_no', 'referral_code')
    list_editable = ('status',)   # change status directly from list!
    readonly_fields = ('created_at', 'extra_data')

@admin.register(PaymentProof)
class PaymentProofAdmin(admin.ModelAdmin):
    list_display  = ('order', 'transaction_id', 'submitted_at')
    search_fields = ('transaction_id', 'order__name')

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display  = ('title', 'is_active')
    list_editable = ('is_active',)

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display  = ('caption', 'is_active')
    list_editable = ('is_active',)


