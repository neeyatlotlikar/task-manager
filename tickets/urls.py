from django.urls import path

from . import views

app_name = "tickets"

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.tickets, name="tickets"),
    path("<int:pk>/", views.ticket_detail, name="ticket_detail"),
]
