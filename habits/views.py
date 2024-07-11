from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializers


class HabitCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт модели Habit на создание.
    """
    serializer_class = HabitSerializers

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.owner = self.request.user
        serializer.save()


class HabitUpdateAPIView(generics.UpdateAPIView):
    """
    Эндпоинт модели Habit на редактирование.
    """
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitListAPIView(generics.ListAPIView):
    """
    Эндпоинт модели Habit на получение списка привычек текущего пользователя.
    """
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = HabitPaginator


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    Эндпоинт модели Habit на получение одного экземпляра.
    """
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """
    Эндпоинт модели Habit на удаление.
    """
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
