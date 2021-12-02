from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework import permissions
from .serializers import *


class RegisterUserView(CreateAPIView):
    # регистрация пользователей
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class CreateReadCounterView(ListCreateAPIView):
    serializer_class = CounterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # разграничение прав доступа к счётчикам(-у)
        current_user = self.request.user
        if current_user.is_staff:
            return Counter.objects.all()
        else:
            return Counter.objects.filter(user=current_user)


class ReadChangeView(RetrieveUpdateAPIView):
    serializer_class = CounterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # разграничение прав доступа к счётчикам(-у)
        if self.request.user.is_staff:
            return Counter.objects.filter(id=self.kwargs.get('pk'))
        else:
            return Counter.objects.filter(id=self.kwargs.get('pk'), user=self.request.user)


class DeleteCounterView(DestroyAPIView):
    # удалить счётчик может только админ
    # чтобы обезопаситься от случайного удаления
    serializer_class = CounterSerializer
    permission_classes = [permissions.IsAdminUser]
