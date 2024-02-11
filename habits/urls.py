from django.urls import path

from habits.views import *
from habits.apps import HabitsConfig

app_name = HabitsConfig.name


urlpatterns = [
    path('', HabitsListAPIView.as_view(), name='habits_list'),
    path('create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('<int:pk>/', HabitRetrieveView.as_view(), name='habit_retrieve'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit_delete'),
]
