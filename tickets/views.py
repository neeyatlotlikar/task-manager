from django.shortcuts import get_object_or_404, render
from .models import SupportTicket


def index(request):
    return render(
        request,
        "tickets/index.html",
        content_type="text/html",
        status=200,
    )


def tickets(request):
    all_tickets = SupportTicket.objects.all().order_by("-created_at")
    return render(
        request,
        "tickets/tickets.html",
        {"tickets": all_tickets},
        content_type="text/html",
        status=200,
    )


def ticket_detail(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)

    return render(
        request,
        "tickets/ticket_details.html",
        {"ticket": ticket},
    )
