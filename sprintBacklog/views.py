from django.shortcuts import render, get_object_or_404
from project.models import Project
from productBacklog.models import PBI
from sprintBacklog.models import Sprint, Task
from django.db.models import Sum

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
		return self.sprint

	# get arg from url
	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		self.sprint = Sprint.objects.filter(sprint_number=kwargs['sprint']).get(project=self.project)
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




































