from typing import ClassVar

from django import forms

from .models import SupportTicket
from accounts.models import User


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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is None:
            raise ValueError("SupportTicketForm requires an authenticated user.")

        self.fields["assigned_to"].queryset = self.get_assignable_users(
            user, self.instance
        )

    @staticmethod
    def get_assignable_users(user: User, instance: SupportTicket | None = None):
        if user.role == "member":
            return User.objects.filter(pk=user.pk)

        if user.role in {"manager", "admin"}:
            queryset = User.objects.filter(role="member")

            if instance and instance.assigned_to:
                queryset = queryset | User.objects.filter(pk=instance.assigned_to_id)

            return queryset.distinct()

        return User.objects.none()


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
