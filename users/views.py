from rest_framework import generics, status
from rest_framework.response import Response

from habits.services import get_chat_id
from users.models import User
from users.serializers import UserSerializer


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        new_user = serializer.save()

        # Хэшируем пароль для нового пользователя
        new_user.set_password(new_user.password)
        # Если введено имя пользователя в Телеграм, то определяем Chat ID пользователя
        if new_user.telegram_name:
            new_user.telegram_chat_id = get_chat_id(new_user.telegram_name)

        new_user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        user = serializer.save()

        # Хэшируем пароль для пользователя, если этот пароль обновляется
        new_password = self.request.data.get('password')
        if new_password:
            user.set_password(new_password)

        # Если обновилось имя пользователя в Телеграм, то определяем Chat ID пользователя
        new_telegram_name = self.request.data.get('telegram_name')
        if new_telegram_name:
            user.telegram_chat_id = get_chat_id(new_telegram_name)

        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
