from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import SupportTicketForm, SupportTicketStatusForm
from .models import SupportTicket


@login_required
def ticket_list(request):
    if request.user.role == "member":
        tickets = SupportTicket.objects.filter(assigned_to=request.user).order_by(
            "-created_at"
        )
    else:
        tickets = SupportTicket.objects.filter(assigned_to__role="member").order_by(
            "-created_at"
        )
    return render(
        request,
        "tickets/ticket_list.html",
        {
            "tickets": tickets,
            "status_choices": SupportTicket.TICKET_STATUS_CHOICES,
        },
    )


@login_required
@permission_required("tickets.add_supportticket", raise_exception=True)
def ticket_create(request):
    if request.method == "POST":
        form = SupportTicketForm(request.POST, user=request.user)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return redirect("tickets:ticket-list")
    else:
        form = SupportTicketForm(user=request.user)

    return render(request, "tickets/ticket_form.html", {"form": form})


@login_required
@permission_required("tickets.change_supportticket", raise_exception=True)
def ticket_update(request, pk):
    if request.user.role == "member":
        ticket = get_object_or_404(SupportTicket, pk=pk, assigned_to=request.user)
    else:
        ticket = get_object_or_404(SupportTicket, pk=pk)

    if request.user.role == "member" and ticket.assigned_to_id != request.user.pk:
        return redirect("tickets:ticket-list")

    if request.method == "POST":
        form = SupportTicketForm(request.POST, instance=ticket, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("tickets:ticket-detail", pk=ticket.pk)
    else:
        form = SupportTicketForm(instance=ticket, user=request.user)

    return render(request, "tickets/ticket_form.html", {"form": form})


@login_required
@permission_required("tickets.change_supportticket", raise_exception=True)
@require_POST
def ticket_status_update(request, pk):
    if request.user.role == "member":
        ticket = get_object_or_404(SupportTicket, pk=pk, assigned_to=request.user)
    else:
        ticket = get_object_or_404(SupportTicket, pk=pk)
    form = SupportTicketStatusForm(request.POST, instance=ticket)
    if not form.is_valid():
        return HttpResponseBadRequest("Invalid ticket status.")
    form.save()
    return redirect("tickets:ticket-list")


@login_required
def ticket_detail(request, pk):
    if request.user.role == "member":
        ticket = get_object_or_404(SupportTicket, pk=pk, assigned_to=request.user)
    else:
        ticket = get_object_or_404(SupportTicket, pk=pk)
    return render(
        request,
        "tickets/ticket_detail.html",
        {
            "ticket": ticket,
            "status_choices": SupportTicket.TICKET_STATUS_CHOICES,
        },
    )


@login_required
@permission_required("tickets.delete_supportticket", raise_exception=True)
def ticket_delete(request, pk):
    if request.user.role == "member":
        ticket = get_object_or_404(SupportTicket, pk=pk, assigned_to=request.user)
    else:
        ticket = get_object_or_404(SupportTicket, pk=pk)

    if request.user.role == "member" and ticket.created_by != request.user:
        return redirect("tickets:ticket_list")

    if request.method == "POST":
        ticket.delete()
        return redirect("tickets:ticket-list")
    return render(request, "tickets/ticket_confirm_delete.html", {"ticket": ticket})
