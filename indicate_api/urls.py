from django.urls import path, include
from .views import *


urlpatterns = [
    path('', include('rest_framework.urls')),
    path('register/', RegisterUserView.as_view()),
    path('counters/', CreateReadCounterView.as_view(), name='details'),
    path('counters/<uuid:pk>', ReadChangeView.as_view()),
    path('counters/delete/<uuid:pk>', DeleteCounterView.as_view()),
]