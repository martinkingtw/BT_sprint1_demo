from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='productBacklog-home'),
    path('about/', views.about, name='productBacklog-about'),
    path('delete/', views.delete, name='productBacklog-delete')
]