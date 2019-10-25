from django.urls import path
from .views import PBListView, PBDetailView
from . import views

urlpatterns = [
    path('', PBListView.as_view(), name='productBacklog-home'),
    path('<int:pk>/', PBDetailView.as_view(), name='productBacklog-detail'),
    path('about/', views.about, name='productBacklog-about'),
    path('create/', views.create_pbi, name='productBacklog-create'),
]