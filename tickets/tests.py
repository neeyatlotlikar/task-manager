from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase

from .forms import SupportTicketForm
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
            created_by=self.user,
        )

    def test_ticket_list_is_a_server_rendered_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test ticket")
        self.assertContains(response, "New ticket")
        self.assertNotContains(response, "hx-")

    def test_member_only_sees_their_own_assigned_tickets(self):
        other_member = User.objects.create_user(
            username="other-member",
            password="test-password-123",
            role="member",
        )
        other_ticket = SupportTicket.objects.create(
            title="Other member ticket",
            description="Assigned elsewhere",
            status="todo",
            assigned_to=other_member,
            created_by=other_member,
        )

        response = self.client.get("/")

        self.assertContains(response, "Test ticket")
        self.assertNotContains(response, other_ticket.title)

    def test_manager_form_only_lists_member_users_for_assignment(self):
        manager = User.objects.create_user(
            username="manager-user",
            password="test-password-123",
            role="manager",
        )
        member = User.objects.create_user(
            username="member-user",
            password="test-password-123",
            role="member",
        )
        admin = User.objects.create_user(
            username="admin-user",
            password="test-password-123",
            role="admin",
        )

        form = SupportTicketForm(user=manager)
        assigned_user_ids = list(
            form.fields["assigned_to"].queryset.values_list("pk", flat=True)
        )

        self.assertIn(member.pk, assigned_user_ids)
        self.assertNotIn(manager.pk, assigned_user_ids)
        self.assertNotIn(admin.pk, assigned_user_ids)

    def test_member_cannot_access_other_users_ticket_details(self):
        other_member = User.objects.create_user(
            username="blocked-member",
            password="test-password-123",
            role="member",
        )
        other_ticket = SupportTicket.objects.create(
            title="Blocked ticket",
            description="Not assigned to this user",
            status="todo",
            assigned_to=other_member,
            created_by=other_member,
        )

        response = self.client.get(f"/tickets/{other_ticket.pk}/")

        self.assertEqual(response.status_code, 404)

    def test_invalid_status_submission_is_rejected_without_updating_ticket(self):
        response = self.client.post(
            f"/tickets/{self.ticket.pk}/status/",
            {"status": "invalid-status"},
        )

        self.assertRedirects(response, "/")
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, "todo")

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
