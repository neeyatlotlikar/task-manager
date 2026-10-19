from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class AuthenticationPageTests(TestCase):
    def test_login_and_signup_render_with_jinja(self):
        login_response = self.client.get("/accounts/login/")
        signup_response = self.client.get("/accounts/signup/")

        self.assertEqual(login_response.status_code, 200)
        self.assertContains(login_response, "Log in")
        self.assertContains(login_response, 'name="csrfmiddlewaretoken"')
        self.assertEqual(signup_response.status_code, 200)
        self.assertContains(signup_response, "Create an account")

    def test_login_honors_a_local_next_url(self):
        User.objects.create_user(username="login-user", password="test-password-123")

        response = self.client.post(
            "/accounts/login/?next=/tickets/create/",
            {
                "username": "login-user",
                "password": "test-password-123",
                "next": "/tickets/create/",
            },
        )

        self.assertRedirects(response, "/tickets/create/", fetch_redirect_response=False)

    def test_external_next_url_is_ignored(self):
        User.objects.create_user(username="login-user", password="test-password-123")

        response = self.client.post(
            "/accounts/login/",
            {
                "username": "login-user",
                "password": "test-password-123",
                "next": "https://example.com/",
            },
        )

        self.assertRedirects(response, "/")

    def test_logout_uses_post(self):
        user = User.objects.create_user(username="logout-user", password="test-password-123")
        self.client.force_login(user)

        self.assertEqual(self.client.get("/accounts/logout/").status_code, 405)

        response = self.client.post("/accounts/logout/")

        self.assertRedirects(response, "/accounts/login/")
