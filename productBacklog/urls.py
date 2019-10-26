from django.urls import path
from .views import (
	PBListView,
	PBDetailView, 
	PBCreateView,
	PBDeleteView
)
from . import views

urlpatterns = [
    path('', PBListView.as_view(), name='productBacklog-home'),
    path('<int:pk>/', PBDetailView.as_view(), name='productBacklog-detail'),
    path('PBI/create/', PBCreateView.as_view(), name='productBacklog-create'),
    path('about/', views.about, name='productBacklog-about'),
    path('delete/<int:pk>', PBDeleteView.as_view(), name='productBacklog-delete'),
]