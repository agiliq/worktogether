from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from datetime import datetime, time

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from teamwork.models import TeamMember, Task, WorkDay


class TeamWorkTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test", email="test@test.com", password="test")

    def test_createtask_perm(self):
        url = reverse('task-create', args=['2016-12-15'])
        response = self.client.post(url, {'task': 'task'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_createtask(self):
        _task = 'Test Task'
        member = create_teammember(self.user)
        self.client.login(username='test', password='test')
        url = reverse('task-create', args=['2016-12-15'])
        self.assertEqual(Task.objects.count(), 0)
        response = self.client.post(url, {'task': _task})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().task, _task)

    def test_retrievetask(self):
        member = create_teammember(self.user)
        today = create_workday(member)
        task = create_task(today, 'task1')
        self.client.login(username='test', password='test')
        url = reverse('task-detail', args=[task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['task'], task.task)

    def test_listteam(self):
        _no = 5
        for i in range(_no):
            _name = "test{}".format(i)
            _email = "test{}@test.com".format(i)
            usr = User.objects.create_user(
                username=_name,
                password=_name,
                email=_email)
            create_teammember(usr, _name, _email)
        self.assertEqual(TeamMember.objects.count(), _no)
        self.client.login(username='test2', password='test2')
        url = reverse('members-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), _no)

    def test_workday(self):
        member = create_teammember(self.user)
        self.client.login(username='test', password='test')
        workday = create_workday(member)
        for i in range(5):
            create_task(workday, "task-{}".format(i))
        self.assertEqual(Task.objects.count(), 5)
        url = reverse('workday-list',
                      args=[datetime.now().strftime('%Y-%m-%d')])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[0]['task_set']), 5)


def create_teammember(user, name='', email=''):
    name = name or 'test'
    email = email or 'test@test.com'
    _time = time(18, 10)
    return TeamMember.objects.create(
        user=user,
        name=name,
        email=email,
        preferred_notifying_time=_time
    )


def create_workday(member, _date=None):
    _date = _date or datetime.now().date()
    return WorkDay.objects.create(
        person=member,
        date=_date
    )


def create_task(day, task):
    return Task.objects.create(task=task, day=day)
