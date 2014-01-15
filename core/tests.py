from django.test import TestCase
import core.models as cm
from django.contrib.auth.models import User

class PersonTestCase(TestCase):
    def setUp(self):
        self.person_1 = build_person()

    def tearDown(self):
        self.person_1.user.delete()
        self.person_1.delete()

    def test_history(self):
        """history models are installed"""
        history = self.person_1.history.all() 
        self.assertNotEqual(history, None)

    def test_touches(self):
        """touch rendering working"""
        self.assertNotEqual(self.person_1.get_touches() , None)

class ProjectTestCase(TestCase):
    def setUp(self):
        self.person_1 = build_person()
        self.project = build_project([self.person_1])

    def tearDown(self):
        self.project.delete()
        self.person_1.user.delete()
        self.person_1.delete()

    def test_history(self):
        """history models are working"""
        self.project.title = 'Beta Project'
        self.project.save()
        history = self.person_1.history.all() 
        self.assertNotEqual(history.count(), 2)


def build_person():
    user = User.objects.create_user(username='john', email='lennon@thebeatles.com', password='johnpassword', first_name='John', last_name='Lennon')
    user.save()
    person = cm.Person(user=user)
    person.save()
    return person

def build_project(members):
    project = cm.Project(title='Alpha Project', brief='here is some text.', medium='TXT', ask=3000)
    project.save()
    for m in members:
        project.members.add(m)
    project.save()
    return project