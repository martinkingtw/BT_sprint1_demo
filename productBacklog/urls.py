from django.urls import path
from .views import (
	PBListView,
	PBDetailView, 
	PBCreateView
)
from . import views

urlpatterns = [
    path('', PBListView.as_view(), name='productBacklog-home'),
    path('<int:pk>/', PBDetailView.as_view(), name='productBacklog-detail'),
    path('PBI/create', PBCreateView.as_view(), name='productBacklog-create'),
    path('about/', views.about, name='productBacklog-about'),
    path('delete/', views.delete, name='productBacklog-delete'),
]