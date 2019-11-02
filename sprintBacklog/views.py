from django.shortcuts import render
from project.models import Project
from productBacklog.models import PBI
from sprintBacklog.models import Sprint

from django.views.generic import (
	ListView, 
	CreateView, 
	DeleteView,
	UpdateView,
	DetailView
)

def home(request, project):
	tmp = {"tmp" : 'tmp'}
	context = {
		'dict': tmp,
		'project': Project.objects.get(slug=project)
	}
	return render(request, 'SprintBacklog/home.html', context)

class SprintBacklogListView(ListView):
	model = Sprint
	template_name = 'sprintBacklog/home.html'
	context_object_name = 'sprint'

	def get_queryset(self):
		return Sprint.objects.filter(pk=3)

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context