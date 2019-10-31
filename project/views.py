from django.shortcuts import render
from django.views.generic import (
	ListView, 
	CreateView, 
	DeleteView
)
from productBacklog.models import Project

class ProjectListView(ListView):
	model = Project
	template_name = 'project/home.html'
	context_object_name = 'projects'

class ProjectCreateView(CreateView):
	model = Project
	fields = ['title',
			'details'
	]
	template_name = 'project/project_form.html'

class ProjectDeleteView(DeleteView):
	model = Project
	template_name = 'project/delete.html'
	slug_url_kwarg = 'project'
	def get_success_url(self):
		return '/'

	# def dispatch(self, request, *args, **kwargs):
	# 	self.project_id = kwargs['fk']
	# 	self.project = get_object_or_404(Project, pk=kwargs['fk'])
	# 	return super().dispatch(request, *args, **kwargs)

	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	context['project'] = self.project
	# 	return context