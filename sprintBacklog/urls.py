from django.urls import path
from .views import (
	SprintBacklogListView,
	)
	# SprintBacklogDetailView, 
	# SprintBacklogCreateView,
	# SprintBacklogDeleteView,
	# SprintBacklogUpdateView
# )
from . import views

urlpatterns = [
    path('<int:sprint>/', SprintBacklogListView.as_view(), name='sprint-home'),
]