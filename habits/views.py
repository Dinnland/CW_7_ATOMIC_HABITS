from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habits
from habits.paginators import HabitsPaginator
from habits.permissions import IsOwner
from habits.serializers.serializers import HabitsSerializer


class HabitsCreateAPIView(generics.CreateAPIView):
    """Создаем урок (Lesson)"""
    serializer_class = HabitsSerializer
    permission_classes = [IsAuthenticated]  # work

    def perform_create(self, serializer):
        new_habit = serializer.save()

        """Пользователь, создавая привычку, автоматически становится ее владельцем"""
        new_habit.user = self.request.user
        new_habit.save()


class HabitsListAPIView(generics.ListAPIView):
    """Получаем список привычкек"""
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = HabitsPaginator

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderator').exists():
            return Habits.objects.all()
        # print(my_task.delay(1))
        return Habits.objects.filter(user=self.request.user)


class PublishedHabitListAPIView(generics.ListAPIView):
    """Получаем список публичных привычек"""
    serializer_class = HabitsSerializer
    queryset = Habits.objects.filter(is_published=True)
    permission_classes = [IsAuthenticated]
    pagination_class = HabitsPaginator


class HabitsRetrieveAPIView(generics.RetrieveAPIView):
    """Получаем 1 привычку по pk"""
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()
    permission_classes = [IsOwner]  # work


class HabitsUpdateAPIView(generics.UpdateAPIView):
    """Обновление привычки по pk"""
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()
    permission_classes = [IsOwner]


class HabitsDestroyAPIView(generics.DestroyAPIView):
    """Удаляем 1 привычку по pk"""
    queryset = Habits.objects.all()
    permission_classes = [IsOwner]  # work
