from django.urls import path
from .views import (
	ProjectListView,
	ProjectCreateView
)
from . import views

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-home'),
    path('create/', ProjectCreateView.as_view(), name='project-create'),
]