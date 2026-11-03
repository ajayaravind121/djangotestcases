from django.test import TestCase, Client
from StuffTracker.models import Stuff, MyUser


class AddItem(TestCase):
    def setUp(self):
        self.client = Client()
        u = MyUser(name="one", password="one")
        u.save()
        Stuff(name="cat", owner=u).save()
        session = self.client.session
        session["name"] = "one"
        session.save()

    def test_item_in_response(self):
        resp = self.client.post("/things/", {"stuff": "hat"})
        self.assertIn("hat", resp.context["things"])
        self.assertIn("cat", resp.context["things"])

    def test_item_in_database(self):
        self.client.post("/things/", {"stuff": "hat"})
        self.assertTrue(Stuff.objects.filter(name="hat", owner__name="one").exists())

    def test_blank_item_not_added(self):
        resp = self.client.post("/things/", {"stuff": ""})
        self.assertEqual(resp.context["things"], ["cat"])