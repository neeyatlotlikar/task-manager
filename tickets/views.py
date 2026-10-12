from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .forms import SupportTicketForm
from .models import SupportTicket


def is_htmx(request):
    return request.headers.get("HX-Request") == "true"


@login_required
def ticket_list(request):
    tickets = SupportTicket.objects.filter(assigned_to=request.user)
    return render(
        request,
        "tickets/ticket_list.html",
        {"tickets": tickets},
    )


@login_required
@permission_required("tickets.add_ticket", raise_exception=True)
def ticket_create(request):
    if request.method == "POST":
        form = SupportTicketForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()

            if is_htmx(request):
                tickets = SupportTicket.objects.filter(assigned_to=request.user)
                return render(
                    request,
                    "tickets/partials/ticket_list_items.html",
                    {"tickets": tickets},
                )

            return redirect("ticket-list")

    else:
        form = SupportTicketForm()

    return render(request, "tickets/partials/ticket_form.html", {"form": form})


@login_required
@permission_required("tickets.change_ticket", raise_exception=True)
def ticket_status_update(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk, assigned_to=request.user)

    if request.method == "POST":
        new_status = request.POST.get("status")

        if new_status in SupportTicket.Status.values:
            ticket.status = new_status
            ticket.save()

        if is_htmx(request):
            return render(
                request,
                "tickets/partials/ticket_row.html",
                {"ticket": ticket},
            )

    return redirect("ticket-list")


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk, assigned_to=request.user)
    return render(request, "tickets/ticket_detail.html", {"ticket": ticket})


@login_required
@permission_required("tickets.change_ticket", raise_exception=True)
def ticket_update(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk, assigned_to=request.user)

    if request.method == "POST":
        form = SupportTicketForm(request.POST, instance=ticket)

        if form.is_valid():
            form.save()

            if is_htmx(request):
                return render(
                    request,
                    "tickets/partials/ticket_row.html",
                    {"ticket": ticket},
                )

            return redirect("ticket-list")

    else:
        form = SupportTicketForm(instance=ticket)

    return render(
        request, "tickets/partials/ticket_form.html", {"form": form, "ticket": ticket}
    )


@login_required
@permission_required("tickets.delete_ticket", raise_exception=True)
def ticket_delete(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk, assigned_to=request.user)

    if request.method == "POST":
        ticket.delete()

        if is_htmx(request):
            tickets = SupportTicket.objects.filter(assigned_to=request.user)
            return render(
                request,
                "tickets/partials/ticket_list_items.html",
                {"tickets": tickets},
            )

        return redirect("ticket-list")

    return render(
        request, "tickets/partials/ticket_confirm_delete.html", {"ticket": ticket}
    )
