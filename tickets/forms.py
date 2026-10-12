from django import forms
from .models import SupportTicket


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ["title", "description", "status", "assigned_to"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 px-4 py-2.5 text-sm focus:border-brand-600 focus:ring-2 focus:ring-brand-100 focus:outline-none",
                    "placeholder": "e.g. Prepare quarterly report",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "w-full rounded-xl border border-slate-300 px-4 py-2.5 text-sm focus:border-brand-600 focus:ring-2 focus:ring-brand-100 focus:outline-none",
                    "placeholder": "Add context, acceptance criteria, or links...",
                }
            ),
            "priority": forms.Select(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm focus:border-brand-600 focus:ring-2 focus:ring-brand-100 focus:outline-none",
                }
            ),
        }
