from django.urls import path
from .views import (
	SprintBacklogListView,
    SprintBacklogCreateView,
    SprintBacklogDetailView,
	)
	# SprintBacklogDetailView,
	# SprintBacklogDeleteView,
	# SprintBacklogUpdateView
# )
from . import views

urlpatterns = [
    path('<int:sprint>/', SprintBacklogListView.as_view(), name='sprint-home'),
    path('noSprint/', views.noSprint ,name='no-sprint'),
    path('create/', SprintBacklogCreateView.as_view(), name='sprintBacklog-create'),
    path('<int:sprint>/', SprintBacklogDetailView.as_view(), name='sprintBacklog-detail'),
]