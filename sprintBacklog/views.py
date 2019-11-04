from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.urls import reverse
from django.http import HttpResponseRedirect

from project.models import Project
from productBacklog.models import PBI
from sprintBacklog.models import Sprint, Task


from django.views.generic import (
	ListView, 
	CreateView, 
	DeleteView,
	UpdateView,
	DetailView
)

def noSprint(request, project):
	context = {
		'project': Project.objects.get(slug=project)
	}
	project = get_object_or_404(Project, slug=project)
	n = Sprint.objects.filter(project=project).count()
	if Sprint.objects.filter(project=project).count() != 0:
		return HttpResponseRedirect(reverse('sprint-home', kwargs={'project': project, 'sprint': n}))	
	
	return render(request, 'SprintBacklog/noSprint.html', context)

class SprintBacklogListView(ListView):
	model = Sprint
	template_name = 'sprintBacklog/home.html'
	context_object_name = 'sprint'

	def get_queryset(self):
		return self.sprint

	# get arg from url
	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		print(kwargs)
		self.sprint = Sprint.objects.get(pk=kwargs['sprint'])
		return super().dispatch(request, *args, **kwargs)

	# pass different queries to html
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		context['all_sprint'] = Sprint.objects.filter(project=self.project).order_by('sprint_number')
		
		task = []
		total = 0
		completed = 0
		for p in PBI.objects.filter(sprint=self.sprint):
			todo = Task.objects.filter(sprint=self.sprint).filter(status='To Do').filter(PBI=p)
			doing = Task.objects.filter(sprint=self.sprint).filter(status='Doing').filter(PBI=p)
			done = Task.objects.filter(sprint=self.sprint).filter(status='Done').filter(PBI=p)
			todoE = todo.aggregate(Sum('effort')).get('effort__sum') if todo else 0
			doingE = doing.aggregate(Sum('effort')).get('effort__sum') if doing else 0
			doneE = done.aggregate(Sum('effort')).get('effort__sum') if done else 0
			total += doneE + doingE + todoE
			completed += doneE
			tmp = {"pbi": p,
					"todo": todo,
					"doing": doing,
					"done": done,
					"finish": doneE,
					"not_finish": doingE + todoE + doneE
					}
			task.append(tmp)

		stat = {"completed": completed,
				"available": self.sprint.available_effort,
				"used": total,
				"remaining": self.sprint.available_effort - total
				}
		context['stat'] = stat
		context['task'] = task
		return context

class SprintBacklogCreateView(CreateView):
	model = Sprint
	fields = [
		"available_effort",
		"duration",
		"details",
	]

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context

	def form_valid(self, form):
		form.instance.project = self.project
		return super().form_valid(form)




































