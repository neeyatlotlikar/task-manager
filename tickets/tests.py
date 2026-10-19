from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase

from .models import SupportTicket

User = get_user_model()


class TicketPageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="ticket-user",
            password="test-password-123",
        )
        self.user.user_permissions.set(
            Permission.objects.filter(
                content_type__app_label="tickets",
                codename__in=[
                    "add_supportticket",
                    "change_supportticket",
                    "delete_supportticket",
                ],
            )
        )
        self.client.force_login(self.user)
        self.ticket = SupportTicket.objects.create(
            title="Test ticket",
            description="Ticket details",
            status="todo",
            assigned_to=self.user,
        )

    def test_ticket_list_is_a_server_rendered_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test ticket")
        self.assertContains(response, "New ticket")
        self.assertNotContains(response, "hx-")

    def test_create_ticket_get_and_post(self):
        response = self.client.get("/tickets/create/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New ticket")

        response = self.client.post(
            "/tickets/create/",
            {
                "title": "Created ticket",
                "description": "Created from the regular form",
                "status": "todo",
                "assigned_to": self.user.pk,
            },
        )

        self.assertRedirects(response, "/")
        self.assertTrue(SupportTicket.objects.filter(title="Created ticket").exists())

    def test_invalid_create_renders_form_errors(self):
        response = self.client.post("/tickets/create/", {})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_update_ticket_post_redirects_to_detail(self):
        response = self.client.post(
            f"/tickets/{self.ticket.pk}/update/",
            {
                "title": "Updated ticket",
                "description": "Updated details",
                "status": "inprogress",
                "assigned_to": self.user.pk,
            },
        )

        self.assertRedirects(response, f"/tickets/{self.ticket.pk}/")
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.title, "Updated ticket")

    def test_ticket_detail_and_status_update(self):
        response = self.client.get(f"/tickets/{self.ticket.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ticket details")

        response = self.client.post(
            f"/tickets/{self.ticket.pk}/status/",
            {"status": "completed"},
        )

        self.assertRedirects(response, "/")
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, "completed")

    def test_delete_requires_confirmation_and_post(self):
        response = self.client.get(f"/tickets/{self.ticket.pk}/delete/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This action cannot be undone.")

        response = self.client.post(f"/tickets/{self.ticket.pk}/delete/")

        self.assertRedirects(response, "/")
        self.assertFalse(SupportTicket.objects.filter(pk=self.ticket.pk).exists())
