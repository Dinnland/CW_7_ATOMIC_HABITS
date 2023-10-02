from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from habits.models import Habits
from users.models import User


# Create your tests here.


class HabitsTestCase(APITestCase):
    """Тестирование сервиса трекера привычек (app Habits)"""
    client_class = APIClient

    def setUp(self):
        """Создание пользователя"""
        self.user = User.objects.create(
            email='test@test.com',
            telegram_chat_id=123456, )
        self.user.set_password('12345678')
        self.user.save()
        # print(f'***********\n{self.user}\n*************')

        self.user2 = User.objects.create(
            email='second_test@test.com',

        )
        self.user2.set_password('12345678')
        self.user2.save()

        """Создание привычки"""
        self.habit = Habits.objects.create(
            time='12:00:00',
            lead_time="00:02:00",
            place='London',
            periodicity='1',
            action='Работать',
            reward=None,
            is_pleasant_habit=False,
            is_published=False,
            related_habit=None,
            user=self.user,
        )
        self.habit2 = Habits.objects.create(
            time='04:00:00',
            lead_time="00:01:00",
            place='Москва',
            periodicity='2',
            action='Умирать',
            reward=None,
            is_pleasant_habit=True,
            is_published=True,
            related_habit=None,
            user=self.user2,
        )
        self.habit3_pleasant = Habits.objects.create(
            time='15:00:00',
            lead_time="00:01:00",
            place='Москва',
            periodicity='2',
            action='Умирать',
            reward=None,
            is_pleasant_habit=False,
            is_published=False,
            related_habit=self.habit2,
            user=self.user,
        )

        """Готовые привычки"""
        # Все хорошо тут
        self.data = {
            "place": "msc",
            "time": "22:47:27.549943",
            "action": "убить",
            "lead_time": "00:02:00",
            "user": self.user.pk,
        }
        # связанная привычка, без признака приятной привычки
        self.data_wrong_related_habit = {
            "place": "msc",
            "time": "23:33:27.549943",
            "action": "скакать",
            "is_pleasant_habit": 'false',
            "periodicity": '1',
            "lead_time": "00:02:00",
            "is_published": 'false',
            "user": self.user.pk,
            "related_habit": self.habit.pk,
        }
        # У привычки не может быть сразу вознаграждения и связанной привычки
        self.data_habit_with_related_and_reward = {
            "place": "кавказ",
            "time": "12:22:27.549943",
            "action": "учиться",
            "is_pleasant_habit": 'false',
            "reward": 'Попить',
            "lead_time": "00:01:00",
            "user": self.user.pk,
            "related_habit": self.habit2.pk,
        }
        # Продолжительность больше чем можно
        self.data_lead_time_wrong = {
            'time': '12:17:00',
            'place': 'дома',
            'action': 'спать',
            "lead_time": "00:04:00",
            "user": self.user.pk,
        }

    def test_get_list(self):
        """Тест вывода привычек"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(path='/habits/')

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,)
        response = response.json()
        self.assertEqual(
            response['results'][0]['time'],
            self.habit.time,)
        self.assertEqual(
            response['results'][0]['place'],
            self.habit.place,
        )
        self.assertEqual(
            response['results'][0]['user'],
            self.user.pk,
        )

    def test_post(self):
        """Тест, где все ОК"""
        self.client.force_authenticate(user=self.user)
        # print(self.client.force_authenticate(user=self.user))
        response = self.client.post('/habits/create/', data=self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_with_data_wrong_related_habit(self):
        """Тест со связанной привычкой, без признака приятной привычки."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            path='/habits/create/', data=self.data_wrong_related_habit, )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, )

    def test_is_enjoyable_habit(self):
        """
        У привычки не может быть сразу вознаграждения и связанной привычки.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            path='/habits/create/', data=self.data_habit_with_related_and_reward,
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
        )

    def test_data_lead_time_wrong(self):
        """Продолжительность больше чем можно."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            path='/habits/create/', data=self.data_lead_time_wrong,
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
        )

    def test_put_update(self):
        """Тест обновления привычки"""
        self.client.force_authenticate(user=self.user)
        pk = Habits.objects.all()[0].pk
        self.data['user'] = self.user.pk

        response = self.client.put(path=f'/habits/update/{pk}/', data=self.data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,)

    def test_anonym_user_cant_create(self):
        """Неавторизованный пользователь не имеет доступа созданию привычек"""
        response = self.client.post(path='/habits/create/', data=self.data)

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
        )

    def test_anonym_user_cant_get_list(self):
        """Неавторизованный пользователь не имеет доступа к привычкам"""
        response = self.client.get(path='/habits/')

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
        )

    def test_anonym_user_cant_get(self):
        """Неавторизованный пользователь не имеет доступа к отдельным привычкам"""
        pk = Habits.objects.all()[0].pk
        response = self.client.get(path=f'/habits/{pk}/')

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
        )

    def test_user_can_get(self):
        """Пользователь имеет доступ"""
        self.client.force_authenticate(user=self.user)

        pk = Habits.objects.all()[0].pk
        response = self.client.get(path=f'/habits/{pk}/')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )

    def test_other_user_cant_get(self):
        """Другой пользователь не имеет доступа"""
        self.client.force_authenticate(user=self.user2)

        pk = Habits.objects.all()[0].pk
        response = self.client.get(path=f'/habits/{pk}/')
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN,
        )

    def tearDown(self):
        pass
