from django.shortcuts import render
from django.views.generic import ListView, CreateView
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