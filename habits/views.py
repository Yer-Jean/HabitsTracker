from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from habits.models import Habit
from habits.paginators import HabitsPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


class GetQuerysetMixin:
    def get_queryset(self):
        if self.request.user.is_authenticated:
            # Возвращаем все публичные привычки и те, которые создал текущий пользователь
            return Habit.objects.filter(is_public=True) | Habit.objects.filter(owner=self.request.user)
        else:
            # Возвращаем только публичные привычки для неавторизованных пользователей
            return Habit.objects.filter(is_public=True)


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HabitsListAPIView(GetQuerysetMixin, generics.ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitsPaginator
    permission_classes = [IsAuthenticatedOrReadOnly]


class HabitRetrieveView(GetQuerysetMixin, generics.RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class HabitUpdateAPIView(generics.UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
