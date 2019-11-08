from django.urls import path
from .views import (
	SprintBacklogListView,
    SprintBacklogCreateView,
    SprintBacklogDetailView,
    SprintBacklogDeleteView,
    SprintBacklogUpdateView,
    TaskCreateView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,

	)
from . import views

urlpatterns = [
    path('<int:sprint>/', SprintBacklogListView.as_view(), name='sprint-home'),
    path('noSprint/', views.noSprint ,name='no-sprint'),
    path('create/', SprintBacklogCreateView.as_view(), name='sprintBacklog-create'),
    path('<int:pk>-detail/', SprintBacklogDetailView.as_view(), name='sprintBacklog-detail'),
    path('<int:pk>-delete/', SprintBacklogDeleteView.as_view(), name='sprintBacklog-delete'),
    path('<int:pk>-edit/', SprintBacklogUpdateView.as_view(), name='sprintBacklog-edit'),
    path('<int:sprint>/<int:PBI>-create/', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>-select/', views.selectPBI, name='sprintBacklog-select'),
    path('<int:pk>/task_edit/', TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/task_detail/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:pk>/task_delete/', TaskDeleteView.as_view(), name='task-delete'),
]