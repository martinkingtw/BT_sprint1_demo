from django.urls import path
from . import views

urlpatterns = [
    path('sprint-<int:sprint>/', views.home, name='sprint-home'),
]