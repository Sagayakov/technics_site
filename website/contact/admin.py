from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'date']
    readonly_fields = ['email', 'date']
    search_fields = ['email']
    list_filter = ['date']
