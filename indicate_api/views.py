from rest_framework.generics import (
    ListCreateAPIView, CreateAPIView, RetrieveUpdateAPIView,
    DestroyAPIView, RetrieveAPIView)
from rest_framework import permissions
from .serializers import *
from django_filters import rest_framework as filters


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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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


class DateFilter(filters.DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return super(DateFilter, self). filter_queryset(request, queryset, view)


class ReadHistory(RetrieveAPIView):
    serializer_class = HistoryDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        """
        пердаём атрибуты из запроса в контекст сериализатора
        для последующей фильтрации
        """
        params = self.request.query_params
        context = {
            'start_date': params.get('start_date', None),
            'end_date': params.get('end_date', None)
        }
        return context

    def get_queryset(self):
        obj = Counter.objects.filter(user=self.request.user, id=self.kwargs.get('pk'))
        return obj

