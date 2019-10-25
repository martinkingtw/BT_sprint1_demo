from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='PBI-home'),
    path('about/', views.about, name='PBI-about'),
]

#comment