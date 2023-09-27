from django.urls import path
from habits.views import *


from habits.apps import HabitsConfig

app_name = HabitsConfig.name

urlpatterns = [
    path('habits/create/', HabitsCreateAPIView.as_view(), name='habits-create'),
    path('habits/', HabitsListAPIView.as_view(), name='habits-list'),
    path('habits/<int:pk>/', HabitsRetrieveAPIView.as_view(), name='habits-retrieve'),
    path('habits/update/<int:pk>/', HabitsUpdateAPIView.as_view(), name='habits-update'),
    path('habits/delete/<int:pk>/', HabitsDestroyAPIView.as_view(), name='habits-delete'),

]
