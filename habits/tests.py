from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@sky.pro',
            is_active=True
        )
        self.user.set_password('123qwe456rty')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.pleasant_habit = Habit.objects.create(
            owner=self.user,
            place='Home',
            action='Drink juice',
            is_pleasant=True
        )
        self.habit = Habit.objects.create(
            owner=self.user,
            place='Home',
            action='Drink water',
            related_action=self.pleasant_habit
        )

    def test_create_habit(self):
        """Habit creation testing"""

        data = {
            'action': 'Meditation',
            'place': 'Home',
            'related_action': self.pleasant_habit.pk
        }
        response = self.client.post(reverse('habits:habit_create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 3)
        self.assertEqual(
            Habit.objects.get(pk=self.habit.pk + 1).owner.email,
            'test@sky.pro'
        )

        data = {
            'action': self.habit.action,
            'place': self.habit.place,
            'related_action': self.pleasant_habit.pk,
            'reward': 'Smile'
        }
        response = self.client.post(reverse('habits:habit_create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": ["You can choose either a pleasant habit or a reward"]
            }
        )

    def test_retrieve_habit(self):
        """Retrieve habit testing"""

        response = self.client.get(reverse('habits:habit_retrieve', kwargs={'pk': self.habit.pk}))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'id': self.habit.pk,
                'owner': self.user.pk,
                'action': 'Drink water',
                'place': 'Home',
                'time': None,
                'duration': '00:02:00',
                'periodicity': 0,
                'reward': None,
                'related_action': self.pleasant_habit.pk,
                'is_pleasant': False,
                'is_public': False,
            }
        )

    def test_update_habit(self):
        """Update habit testing"""

        data = {
            'place': 'Office'
        }
        response = self.client.patch(
            reverse('habits:habit_update', kwargs={'pk': self.habit.pk}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json()['place'],
            'Office'
        )

    def test_list_habit(self):
        """List habit testing"""

        response = self.client.get(reverse('habits:habits_list'))

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['count'], 2
        )

    def test_destroy_habit(self):
        """Habit deleting testing"""

        response = self.client.delete(
            reverse('habits:habit_delete', kwargs={'pk': self.habit.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        with self.assertRaises(ObjectDoesNotExist):
            Habit.objects.get(pk=self.habit.pk)
