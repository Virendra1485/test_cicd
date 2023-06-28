from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .views import UserSigninView
from account.models import User
from django.contrib.messages import get_messages
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.auth.forms import AuthenticationForm
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .views import UserSigninView


class UserSignupViewTestCase(TestCase):
    def setUp(self):
        self.signup_url = reverse("signup")
        self.signin_url = reverse("signin")
        self.user_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "longitude": "123.456",
            "latitude": "78.910",
        }

    def test_signup_view_success(self):
        response = self.client.post(self.signup_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.signin_url)

        User = get_user_model()
        user = User.objects.get(username=self.user_data["username"])
        self.assertEqual(user.location.x, float(self.user_data["longitude"]))
        self.assertEqual(user.location.y, float(self.user_data["latitude"]))

    def test_signup_view_invalid_form(self):
        invalid_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.signup_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "longitude", "This field is required.")
        self.assertFormError(response, "form", "latitude", "This field is required.")

        User = get_user_model()
        self.assertFalse(
            User.objects.filter(username=self.user_data["username"]).exists()
        )
