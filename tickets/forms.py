from typing import ClassVar

from django import forms

from .models import SupportTicket


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields: ClassVar[list[str]] = ["title", "description", "status", "assigned_to"]
        widgets: ClassVar[dict[str, forms.Widget]] = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-100",
                    "placeholder": "e.g. Prepare quarterly report",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-100",
                    "placeholder": "Add context, acceptance criteria, or links...",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-100",
                }
            ),
            "assigned_to": forms.Select(
                attrs={
                    "class": "w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-100",
                }
            ),
        }


class SupportTicketStatusForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields: ClassVar[list[str]] = ["status"]
        widgets: ClassVar[dict[str, forms.Widget]] = {
            "status": forms.Select(
                attrs={
                    "class": "rounded-md border border-slate-300 bg-white px-2 py-1 text-sm",
                }
            ),
        }
