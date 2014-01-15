from django.test import TestCase
import core.models as cm
from django.contrib.auth.models import User

class PersonTestCase(TestCase):
    def setUp(self):
        self.person = build_person()

    def test_history(self):
        """history models are working"""
        history = self.person.history.all() 
        self.assertNotEqual(history, None)

    def test_touches(self):
        """history models are working"""
        self.assertNotEqual(self.person.get_touches() , None)

def build_person():
    user = User.objects.create_user(username='john', email='lennon@thebeatles.com', password='johnpassword', first_name='John', last_name='Lennon')
    person = cm.Person(user=user)
    return person