from django.urls import path

from . import views

app_name = "tickets"

urlpatterns = [
    path("", views.ticket_list, name="ticket-list"),
    path("tickets/create/", views.ticket_create_or_update, name="ticket-create"),
    path("tickets/<int:pk>/", views.ticket_detail, name="ticket-detail"),
    path("tickets/<int:pk>/update/", views.ticket_create_or_update, name="ticket-update"),
    path("tickets/<int:pk>/delete/", views.ticket_delete, name="ticket-delete"),
    path("tickets/<int:pk>/status/", views.ticket_status_update, name="ticket-status"),
]
