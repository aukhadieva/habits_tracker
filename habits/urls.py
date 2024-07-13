from django.urls import path

from habits.apps import HabitsConfig
from habits.views import (
    HabitCreateAPIView,
    HabitUpdateAPIView,
    HabitPrivetListAPIView,
    HabitRetrieveAPIView,
    HabitDestroyAPIView,
    HabitPublicListAPIView,
)

app_name = HabitsConfig.name

urlpatterns = [
    path("create_habit/", HabitCreateAPIView.as_view(), name="create_habit"),
    path("edit_habit/<int:pk>/", HabitUpdateAPIView.as_view(), name="edit_habit"),
    path("", HabitPrivetListAPIView.as_view(), name="habits"),
    path("public_habits/", HabitPublicListAPIView.as_view(), name="public_habits"),
    path("habit/<int:pk>/", HabitRetrieveAPIView.as_view(), name="habit"),
    path("delete_habit/<int:pk>/", HabitDestroyAPIView.as_view(), name="delete_habit"),
]
