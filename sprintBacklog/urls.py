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
    path('<int:pk>-start/', views.start, name='sprintBacklog-start'),
    path('<int:pk>-end/', views.end, name='sprintBacklog-end'),

    path('<int:sprint>/<int:PBI>-create/', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>-select/', views.selectPBI, name='sprintBacklog-select'),
    path('<int:sprint>-removePBI/<int:pk>', views.removePBI, name='sprintBacklog-remove'),
    path('<int:sprint>/task_edit/<int:pk>', TaskUpdateView.as_view(), name='task-update'),
    path('<int:sprint>/task_detail/<int:pk>', TaskDetailView.as_view(), name='task-detail'),
    path('<int:sprint>/task_delete/<int:pk>', TaskDeleteView.as_view(), name='task-delete'),
]