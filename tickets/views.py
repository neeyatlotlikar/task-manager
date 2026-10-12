from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import SupportTicket


@login_required
def ticket_list(request):
    all_tickets = SupportTicket.objects.all().order_by("-created_at")
    return render(
        request,
        "tickets/ticket_list.html",
        {"tickets": all_tickets},
        content_type="text/html",
        status=200,
    )


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)

    return render(
        request,
        "tickets/ticket_details.html",
        {"ticket": ticket},
    )
