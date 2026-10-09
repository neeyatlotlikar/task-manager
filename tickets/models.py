from django.db import models


class TicketStatus(models.TextChoices):
    todo = "todo", "To-Do"
    inprogress = "inprogress", "In Progress"
    onhold = "onhold", "On hold"
    completed = "completed", "Completed"


class SupportTicket(models.Model):
    title = models.CharField(max_length=200)
    # TODO: assigned_to = User()
    description = models.TextField("Details about the ticket")
    status = models.CharField(
        max_length=20,
        choices=TicketStatus,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
