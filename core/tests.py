from django.test import TestCase
import core.models as cm
from django.contrib.auth.models import User


class ProjectTestCase(TestCase):
    def setUp(self):
        self.users = [build_user()]
        self.projects = [build_project([self.users[0]])]

    def tearDown(self):
        for p in self.projects:
            p.delete()
        for u in self.users:
            u.delete()

    def test_history(self):
        """history models are working"""
        self.projects[0].title = 'Beta Project'
        self.projects[0].save()
        history = self.users[0].history.all() 
        self.assertNotEqual(history.count(), 2)


def build_user():
    user = User.objects.create_user(username='john', email='lennon@thebeatles.com', password='johnpassword', first_name='John', last_name='Lennon')
    user.save()
    return user

def build_project(members):
    project = cm.Project(title='Alpha Project', brief='here is some text.', medium='TXT', ask=3000)
    project.save()
    for m in members:
        project.members.add(m)
    project.save()
    return project