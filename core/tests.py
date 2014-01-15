from django.test import TestCase
import core.models as cm
from django.contrib.auth.models import User

class PersonTestCase(TestCase):
    def setUp(self):
        self.person = build_person()

    def test_history(self):
        """history models are working"""
        history = self.person.history() 
        self.assertNotEqual(history, None)

def build_person():
    user = User.objects.create_user(username='john', email='lennon@thebeatles.com', password='johnpassword', first_name='John', last_name='Lennon')
    person = cm.Person(user=user)
    return person