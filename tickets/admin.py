from django.contrib import admin

from .models import SupportTicket


@admin.register(SupportTicket)
class SupportTicketsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("status",)
    search_fields = (
        "title",
        "description",
    )
