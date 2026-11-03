from django.test import TestCase, Client
from StuffTracker.models import Stuff, MyUser


class LoginFail(TestCase):
    def setUp(self):
        self.client = Client()
        for name in ["one", "two"]:
            u = MyUser(name=name, password=name)
            u.save()
            Stuff(name="cat", owner=u).save()

    def test_wrong_password(self):
        resp = self.client.post("/", {"name": "one", "password": "wrong"}, follow=True)
        self.assertEqual(resp.context["message"], "bad password")
        self.assertTemplateUsed(resp, "home.html")
        self.assertEqual(resp.redirect_chain, [])

    def test_blank_password(self):
        resp = self.client.post("/", {"name": "one", "password": ""}, follow=True)
        self.assertEqual(resp.context["message"], "bad password")

    def test_other_users_password(self):
        resp = self.client.post("/", {"name": "one", "password": "two"}, follow=True)
        self.assertEqual(resp.context["message"], "bad password")

    def test_no_session_on_failure(self):
        self.client.post("/", {"name": "one", "password": "wrong"})
        self.assertNotIn("name", self.client.session)