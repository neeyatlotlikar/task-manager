from django.db import models

from config import settings


class SupportTicket(models.Model):
    TICKET_STATUS_CHOICES = (
        ("todo", "To-Do"),
        ("inprogress", "In Progress"),
        ("onhold", "On hold"),
        ("completed", "Completed"),
    )

    title = models.CharField(max_length=200)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tickets",
        default=None,
    )
    description = models.TextField("Details about the ticket")
    status = models.CharField(
        max_length=20,
        choices=TICKET_STATUS_CHOICES,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_tickets",
        default=None,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
