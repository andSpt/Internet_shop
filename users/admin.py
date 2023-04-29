from django.contrib import admin
from users.models import *
from products.admin import BasketAdmin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']
    inlines = [BasketAdmin]

@admin.register(EmailVerification)
class EmailVerification(admin.ModelAdmin):
    list_display = ['code', 'user', 'expiration']
    fields = ['code', 'user', 'expiration', 'created']
    readonly_fields = ['created']
