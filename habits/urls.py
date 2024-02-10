from django.urls import path

from habits.views import *
from habits.apps import HabitsConfig

app_name = HabitsConfig.name


urlpatterns = [
    # path('', HabitsListAPIView.as_view(), name='habits_list'),
    path('create/', HabitCreateAPIView.as_view(), name='habit_create'),
]
