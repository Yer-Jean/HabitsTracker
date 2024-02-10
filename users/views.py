from rest_framework import generics

from users.models import User
from users.serializers import UserSerializer


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        new_user = serializer.save()
        # Хэшируем пароль для нового пользователя
        new_user.set_password(new_user.password)
        new_user.save()


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        user = serializer.save()
        # Хэшируем пароль для пользователя, если этот пароль обновляется
        new_password = self.request.data.get('password')
        if new_password:
            user.set_password(new_password)
        user.save()
