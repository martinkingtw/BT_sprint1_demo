from django.urls import path
from .views import (
	TodoPBListView,
    AllPBListView,
	PBDetailView, 
	PBCreateView,
	PBDeleteView,
	PBUpdateView
)
from . import views

urlpatterns = [
    path('unfinished/', TodoPBListView.as_view(), name='productBacklog-home'),
    path('all/', AllPBListView.as_view(), name='productBacklog-all'),
    path('<int:pk>/', PBDetailView.as_view(), name='productBacklog-detail'),
    path('create/', PBCreateView.as_view(), name='productBacklog-create'),
    path('<int:pk>-edit/', PBUpdateView.as_view(), name='productBacklog-update'),
    path('<int:pk>-delete/', PBDeleteView.as_view(), name='productBacklog-delete'),
]