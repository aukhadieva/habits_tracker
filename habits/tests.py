from django.urls import reverse
from rest_framework import test, status

from habits.models import Habit
from users.models import User


class HabitTestCase(test.APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@bk.ru", password=123, tg_chat_id="123"
        )
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            owner=self.user, behavior="test", time="2024-07-16 22:08:00+05", location="test"
        )

    def test_habit_create(self):
        """
        Тест на создание привычки.
        """
        url = reverse("habits:create_habit")
        data = {
            "owner": self.user.pk,
            "behavior": "test2",
            "time": "2024-07-16 23:08:00+05",
            "location": "test2",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_update(self):
        """
        Тест на обновление привычки.
        """
        url = reverse("habits:edit_habit", args=(self.habit.pk,))
        data = {
            "owner": self.user.pk,
            "behavior": "test2",
            "time": "2024-07-16 23:08:00+05",
            "location": "test2",
            "frequency": 1,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("time"), "2024-07-16 23:08:00+05")

    def test_habit_list(self):
        """
        Тест на получение списка привычек.
        """
        url = reverse("habits:habits")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "behavior": self.habit.behavior,
                    "time": data["results"][0]["time"],
                    "location": self.habit.location,
                    "frequency": 1,
                    "award": None,
                    "duration": "00:02:00",
                    "is_pleasant_habit": False,
                    "is_public": None,
                    "owner": self.user.pk,
                    "related_habit": None,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_habit_public_list(self):
        """
        Тест на получение списка публичных привычек.
        """
        url = reverse("habits:public_habits")
        response = self.client.get(url)
        data = response.json()
        result = {"count": 0, "next": None, "previous": None, "results": []}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_habit_retrieve(self):
        """
        Тест на получение одной привычки.
        """
        url = reverse("habits:habit", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("location"), self.habit.location)

    def test_habit_destroy(self):
        """
        Тест на удаление одной привычки.
        """
        url = reverse("habits:delete_habit", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)
