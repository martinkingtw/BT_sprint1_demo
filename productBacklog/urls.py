from django.urls import path
from .views import (
	PBListView,
	PBDetailView, 
	PBCreateView,
	PBDeleteView,
	PBUpdateView
)
from . import views

urlpatterns = [
    path('', PBListView.as_view(), name='productBacklog-home'),
    path('<int:pk>/', PBDetailView.as_view(), name='productBacklog-detail'),
    path('create/', PBCreateView.as_view(), name='productBacklog-create'),
    path('<int:pk>-edit/', PBUpdateView.as_view(), name='productBacklog-update'),
    path('about/', views.about, name='productBacklog-about'),
    path('<int:pk>-delete/', PBDeleteView.as_view(), name='productBacklog-delete'),
]