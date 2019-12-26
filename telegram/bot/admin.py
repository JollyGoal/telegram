from django.contrib import admin

from .models import Profile, Transaction, VerifiedTransaction


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'balance', 'invited_by', 'first_name', 'last_name')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('broker', 'card', 'type', 'sum', 'image', 'pub_date', 'verified')


class VerifiedTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'verified_sum', 'pub_date')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(VerifiedTransaction, VerifiedTransactionAdmin)
