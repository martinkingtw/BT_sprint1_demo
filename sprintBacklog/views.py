from django.shortcuts import render
from project.models import Project
# Create your views here.
def home(request, project):
	tmp = {"tmp" : 'tmp'}
	context = {
		'dict': tmp,
		'project': Project.objects.get(slug=project)
	}
	return render(request, 'SprintBacklog/home.html', context)