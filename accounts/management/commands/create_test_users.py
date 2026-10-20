from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from tickets.models import SupportTicket

User = get_user_model()


TEST_USERS = [
    {
        "username": "test_admin",
        "first_name": "Test",
        "last_name": "Admin",
        "email": "test_admin@example.com",
        "password": "AdminPass123!",
        "role": "admin",
        "is_staff": True,
        "is_superuser": True,
    },
    {
        "username": "test_manager",
        "first_name": "Test",
        "last_name": "Manager",
        "email": "test_manager@example.com",
        "password": "ManagerPass123!",
        "role": "manager",
        "is_staff": False,
        "is_superuser": False,
    },
    {
        "username": "test_member",
        "first_name": "Test",
        "last_name": "Member",
        "email": "test_member@example.com",
        "password": "MemberPass123!",
        "role": "member",
        "is_staff": False,
        "is_superuser": False,
    },
    {
        "username": "test_member2",
        "first_name": "Test",
        "last_name": "Member2",
        "email": "test_member2@example.com",
        "password": "MemberPass123!",
        "role": "member",
        "is_staff": False,
        "is_superuser": False,
    },
    {
        "username": "test_member3",
        "first_name": "Test",
        "last_name": "Member3",
        "email": "test_member3@example.com",
        "password": "MemberPass123!",
        "role": "member",
        "is_staff": False,
        "is_superuser": False,
    },
]


def get_ticket_permissions(*codenames):
    content_type = ContentType.objects.get_for_model(SupportTicket)

    return list(
        Permission.objects.filter(
            content_type=content_type,
            codename__in=codenames,
        )
    )


class Command(BaseCommand):
    help = (
        "Create permission groups and test users for admin, manager, and member roles."
    )

    def handle(self, *args, **options):
        self.stdout.write("Creating role permission groups...")

        self.create_groups()
        self.create_users()

        self.stdout.write(
            self.style.SUCCESS("Test users and groups created successfully.")
        )

    def create_groups(self):
        ticket_permissions = {
            "add": get_ticket_permissions("add_supportticket"),
            "change": get_ticket_permissions("change_supportticket"),
            "delete": get_ticket_permissions("delete_supportticket"),
        }

        manager_group, _ = Group.objects.get_or_create(name="Manager")
        member_group, _ = Group.objects.get_or_create(name="Member")

        # Managers can create tickets for other users and assign them,
        # but do not receive CRUD permissions over member accounts.
        manager_group.permissions.set(
            ticket_permissions["add"]
            + ticket_permissions["change"]
            + ticket_permissions["delete"]
        )

        # Members can CRUD only their own personal data. Model-level permissions
        # allow the action; object-level filtering must be enforced in views.
        member_group.permissions.set(
            ticket_permissions["add"]
            + ticket_permissions["change"]
            + ticket_permissions["delete"]
        )

        self.stdout.write("Created/updated groups: Manager, Member")

    def create_users(self):
        groups = {
            "manager": Group.objects.get(name="Manager"),
            "member": Group.objects.get(name="Member"),
        }

        for user_data in TEST_USERS:
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults={
                    "email": user_data["email"],
                    "role": user_data["role"],
                    "is_staff": user_data["is_staff"],
                    "is_superuser": user_data["is_superuser"],
                },
            )

            user.email = user_data["email"]
            user.role = user_data["role"]
            user.is_staff = user_data["is_staff"]
            user.is_superuser = user_data["is_superuser"]
            user.set_password(user_data["password"])
            user.save()

            user.groups.clear()

            if user.role in groups:
                user.groups.add(groups[user.role])

            status = "Created" if created else "Updated"
            self.stdout.write(
                f"{status}: {user.username} ({user.role}) | password: {user_data['password']}"
            )
