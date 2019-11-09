from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.urls import reverse
from django.http import HttpResponseRedirect

from project.models import Project
from productBacklog.models import PBI
from sprintBacklog.models import Sprint, Task
from datetime import timedelta, date


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
	if Sprint.objects.filter(project=project).count() != 0:
		n = Sprint.objects.filter(project=project).order_by('pk').last().pk
		return HttpResponseRedirect(reverse('sprint-home', kwargs={'project': project.slug, 'sprint': n}))
	
	return render(request, 'SprintBacklog/noSprint.html', context)

class SprintBacklogListView(ListView):
	model = Sprint
	template_name = 'sprintBacklog/home.html'
	context_object_name = 'sprint'

	def get_queryset(self):
		queryset = Sprint.objects.filter(project_id=self.project).order_by('pk')
		index = 1
		for s in queryset:
			s.title = "Sprint" + str(index)
			s.save()
			index += 1

		today = date.today()
		for obj in PBI.objects.filter(sprint=self.sprint):
			todo = Task.objects.filter(status='To Do', PBI=obj, sprint=obj.sprint.order_by('start_date').last())
			doing = Task.objects.filter(status='Doing', PBI=obj, sprint=obj.sprint.order_by('start_date').last())
			done = Task.objects.filter(status='Done', PBI=obj, sprint=obj.sprint.order_by('start_date').last())

			if today - obj.sprint.order_by('start_date').last().start_date >= timedelta(weeks=self.project.duration):
				if todo or doing:
					obj.status = 'To Do'
					obj.save()
				elif done and not todo and not doing:
					obj.status = 'Done'
					obj.save()
			else:
				if done and not todo and not doing:
					obj.status = 'Done'
					obj.save()

		return self.sprint

	# get arg from url
	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		self.sprint = Sprint.objects.get(pk=kwargs['sprint'])
		return super().dispatch(request, *args, **kwargs)

	# pass different queries to html
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		context['all_sprint'] = Sprint.objects.filter(project=self.project).order_by('pk')
		context['PBI'] = PBI.objects.filter(project=self.project, status='To Do')
		
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

class SprintBacklogDetailView(DetailView):
	model = Sprint
	template_name = 'sprintBacklog/detail.html'
	context_object_name = 'sprint'

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		self.sprint = Sprint.objects.get(pk=kwargs['pk'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		context['sprint'] = self.sprint

		task = []
		for p in PBI.objects.filter(sprint=self.sprint):
			todo = Task.objects.filter(sprint=self.sprint).filter(status='To Do').filter(PBI=p)
			doing = Task.objects.filter(sprint=self.sprint).filter(status='Doing').filter(PBI=p)
			done = Task.objects.filter(sprint=self.sprint).filter(status='Done').filter(PBI=p)
			todoE = todo.aggregate(Sum('effort')).get('effort__sum') if todo else 0
			doingE = doing.aggregate(Sum('effort')).get('effort__sum') if doing else 0
			doneE = done.aggregate(Sum('effort')).get('effort__sum') if done else 0
			tmp = {"pbi": p,
				   "todo": todo,
				   "doing": doing,
				   "done": done,
				   "finish": doneE,
				   "not_finish": doingE + todoE + doneE
				   }
			task.append(tmp)
		context['task'] = task

		return context

class SprintBacklogDeleteView(DeleteView):
	model = Sprint
	template_name = 'sprintBacklog/delete.html'

	def get_success_url(self):
		all_sprint = Sprint.objects.filter(project=self.project).order_by('-pk')
		number_of_sprint = all_sprint.count()
		if number_of_sprint == 1:
			return '/' + str(self.project.slug) + '-sprint_noSprint'
		elif all_sprint.first().pk != self.sprint.pk:
			return '/' + str(self.project.slug) + '-sprint_' + str(all_sprint.first().pk)
		else:
			return '/' + str(self.project.slug) + '-sprint_' + str(all_sprint[1].pk)

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		self.sprint = Sprint.objects.get(pk=kwargs['pk'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context

class SprintBacklogUpdateView(UpdateView):
	model = Sprint
	fields = [
		"available_effort",
		"details",
	]

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context

class TaskCreateView(CreateView):
	model = Task
	fields = [
		'title',
		'effort',
		'task_owner',
		'details',
	]
	template_name = 'sprintBacklog/task_form.html'

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		self.sprint = Sprint.objects.get(pk=kwargs['sprint'])
		self.PBI = PBI.objects.get(pk=kwargs['PBI'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['PBI'] = self.PBI
		context['project'] = self.project
		return context

	def form_valid(self, form):
		form.instance.sprint = self.sprint
		form.instance.PBI = self.PBI
		return super(TaskCreateView, self).form_valid(form)




class TaskDetailView(DetailView):
	model = Task
	template_name = 'sprintBacklog/taskdetail.html'
	context_object_name = 'task'


	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		self.sprint = Sprint.objects.get(pk=kwargs['sprint'])
		# self.PBI = PBI.objects.get(pk=kwargs['PBI'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# context['PBI'] = self.PBI
		context['sprint'] = self.sprint
		context['project'] = self.project
		return context



class TaskUpdateView(UpdateView):
	model =  Task
	fields = [
		'title',
		'task_owner',
		'status',
		'effort',
		'details',
	]

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context


class TaskDeleteView(DeleteView):
	model = Task
	template_name = 'sprintBacklog/taskdelete.html'
	context_object_name = 'task'

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		self.sprint = Sprint.objects.get(pk=kwargs['sprint'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context

	def get_success_url(self):
		return '/' + str(self.project.slug) + '-sprint_' + str(self.sprint.pk)


def selectPBI(request, project, pk):
	context = {
		'project': Project.objects.get(slug=project),
		'sprint': Sprint.objects.get(pk=pk),
		'PBI': PBI.objects.filter(project=Project.objects.get(slug=project), status='To Do'),
	}
	if request.POST:
		print(request.POST.getlist('PBIs'))
		for id in request.POST.getlist('PBIs'):
			print(id)
			selectedPBI = PBI.objects.get(pk=id)
			selectedPBI.sprint.add(Sprint.objects.get(pk=pk))
			selectedPBI.status = 'Doing'
			selectedPBI.save()
		return HttpResponseRedirect(reverse('sprint-home', kwargs={'project': project, 'sprint': pk}))
	return render(request, 'sprintBacklog/selectPBI.html', context)

def removePBI(request, project, sprint, pk):
	context = {
		'project': Project.objects.get(slug=project),
		'sprint': Sprint.objects.get(pk=sprint),
	}
	if request.POST:
		tmp = PBI.objects.get(pk=pk)
		tmp.sprint.remove(Sprint.objects.get(pk=sprint))
		tmp.status = 'To Do'
		Task.objects.filter(PBI=PBI.objects.get(pk=pk)).delete()
		tmp.save()
		return HttpResponseRedirect(reverse('sprint-home', kwargs={'project': project, 'sprint': sprint}))

	return render(request, 'sprintBacklog/removePBI.html', context)


