from django import forms
from .models import SupportTicket


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ["title", "description", "status", "assigned_to"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full rounded-md border-slate-300 dark:border-slate-600 dark:bg-slate-800",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "w-full rounded-md border-slate-300 dark:border-slate-600 dark:bg-slate-800",
                }
            ),
        }
