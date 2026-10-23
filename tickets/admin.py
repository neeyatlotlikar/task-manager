from typing import ClassVar

from django import forms
from django.contrib import admin
from import_export.admin import ExportMixin
from import_export.forms import ExportForm

from .models import SupportTicket
from .resources import SupportTicketResource


class SupportTicketDateRangeExportForm(ExportForm):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Created from",
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Created to",
    )


@admin.register(SupportTicket)
class SupportTicketsAdmin(ExportMixin, admin.ModelAdmin):
    resource_classes: ClassVar = [SupportTicketResource]
    export_form_class = SupportTicketDateRangeExportForm
    list_display = (
        "id",
        "title",
        "status",
        "assigned_to",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "assigned_to", "created_at", "updated_at")
    search_fields = (
        "title",
        "description",
    )
    date_hierarchy = "created_at"

    def get_export_resource_kwargs(self, request, **kwargs):
        kwargs = super().get_export_resource_kwargs(request, **kwargs)

        export_form = kwargs.get("export_form")
        if export_form:
            kwargs["start_date"] = export_form.cleaned_data.get("start_date")
            kwargs["end_date"] = export_form.cleaned_data.get("end_date")

        return kwargs


@admin.register(SupportTicket.history.model)
class HistoricalSupportTicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "history_type",
        "history_user",
        "history_date",
        "assigned_to",
    )
    list_filter = ("history_type", "status", "assigned_to", "created_at", "updated_at")
    search_fields = (
        "title",
        "description",
    )
    readonly_fields: ClassVar = [
        field.name for field in SupportTicket.history.model._meta.fields
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
