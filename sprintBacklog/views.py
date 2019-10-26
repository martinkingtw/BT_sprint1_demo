from django.shortcuts import render
from project.models import Project
# Create your views here.
def home(request, fk):
	tmp = {"tmp" : 'tmp'}
	context = {
		'dict': tmp,
		'project': Project.objects.get(pk=fk)
	}
	return render(request, 'SprintBacklog/home.html', context)