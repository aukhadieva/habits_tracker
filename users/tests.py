from django.urls import reverse
from rest_framework import test, status

from users.models import User


class UserTestCase(test.APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@bk.ru", password=123, tg_chat_id="123"
        )
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        """
        Тест на создание пользователя.
        """
        url = reverse("users:users-list")
        data = {"email": "test1@bk.ru", "password": 1234, "tg_chat_id": "123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_user_update(self):
        """
        Тест на обновление пользователя.
        """
        url = reverse("users:users-detail", args=(self.user.pk,))
        data = {"email": "test1@bk.ru", "password": 123, "tg_chat_id": "123"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), "test1@bk.ru")

    def test_user_list(self):
        """
        Тест на получение списка пользователей.
        """
        url = reverse("users:users-list")
        response = self.client.get(url)
        data = response.json()
        result = [{"email": "test@bk.ru", "password": "123"}]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_user_retrieve(self):
        """
        Тест на получение одного пользователя.
        """
        url = reverse("users:users-detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), self.user.email)

    def test_user_destroy(self):
        """
        Тест на удаление одного пользователя.
        """
        url = reverse("users:users-detail", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)
