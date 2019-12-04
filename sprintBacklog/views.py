from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Q
from django.urls import reverse
from django.http import HttpResponseRedirect

from project.models import Project
from productBacklog.models import PBI
from sprintBacklog.models import Sprint, Task
from sprintBacklog.forms import TaskForm, TaskCreateForm
from datetime import timedelta, date

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from django.views.generic import (
	ListView, 
	CreateView, 
	DeleteView,
	UpdateView,
	DetailView
)

def start(request, project, pk):
	sprint = Sprint.objects.get(pk=pk)
	if request.POST:
		sprint.startSprint()
		return HttpResponseRedirect(reverse('sprint-home', kwargs={'project': project, 'sprint': pk}))
	return HttpResponseRedirect(reverse('sprint-home', kwargs={'project': project, 'sprint': pk}))

def end(request, project, pk):
	sprint = Sprint.objects.get(pk=pk)
	if request.POST:
		sprint.endSprint()
		return HttpResponseRedirect(reverse('sprint-home', kwargs={'project': project, 'sprint': pk}))
	return HttpResponseRedirect(reverse('sprint-home', kwargs={'project': project, 'sprint': pk}))


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
		queryset = Sprint.objects.filter(project=self.project).order_by('pk')
		index = 1
		for s in queryset:
			s.title = "Sprint" + str(index)
			s.save()
			index += 1
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
		context['lastSprintEnded'] = Sprint.objects.filter(project=self.project).order_by('pk').last().status == 'Ended'
		
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

class SprintBacklogCreateView(UserPassesTestMixin,CreateView):
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

	def test_func(self):
		if self.request.user.position == '3':
			return True
		return False

class SprintBacklogDetailView(DetailView):
	model = Sprint
	template_name = 'sprintBacklog/detail.html'
	context_object_name = 'sprint'

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		self.sprint = Sprint.objects.get(pk=kwargs['pk'])
		print(self.sprint.editable())
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		context['sprint'] = self.sprint
		context['editable'] = self.sprint.editable()

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

class SprintBacklogDeleteView(UserPassesTestMixin,DeleteView):
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

	def post(self, request, *args, **kwargs):
		PBI.objects.filter(sprint = self.sprint).update(status='To Do')
		return super().post(request, *args, **kwargs)

	def test_func(self):
		if self.request.user.position == '3':
			return True
		return False

class SprintBacklogUpdateView(UserPassesTestMixin,UpdateView):
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

	def test_func(self):
		if self.request.user.position == '3':
			return True
		return False




class TaskDetailView(DetailView):
	model = Task
	template_name = 'sprintBacklog/taskdetail.html'
	context_object_name = 'task'


	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		self.sprint = Sprint.objects.get(pk=kwargs['sprint'])
		# self.PBI = PBI.objects.get(pk=kwargs['PBI'])
		self.task = Task.objects.get(pk=kwargs['pk'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# context['PBI'] = self.PBI
		context['sprint'] = self.sprint
		context['project'] = self.project
		context['editable'] = self.task.editable()
		return context

class TaskCreateView(CreateView):
	model = Task
	form_class = TaskCreateForm
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

	def get_form_kwargs(self, **kwargs):
		form_kwargs = super(TaskCreateView, self).get_form_kwargs(**kwargs)
		form_kwargs["project"] = self.project
		return form_kwargs



class TaskUpdateView(UserPassesTestMixin,UpdateView):
	model =  Task
	form_class = TaskForm

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context

	def test_func(self):
		task = self.get_object()
		if task.task_owner == self.request.user or task.task_owner == None:
			return True
		return False

	def get_form_kwargs(self, **kwargs):
		form_kwargs = super(TaskUpdateView, self).get_form_kwargs(**kwargs)
		form_kwargs["project"] = self.project
		return form_kwargs


class TaskDeleteView(UserPassesTestMixin,DeleteView):
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

	def test_func(self):
		task = self.get_object()
		if task.task_owner == self.request.user or task.task_owner == None:
			return True
		return False


def selectPBI(request, project, pk):
	context = {
		'project': Project.objects.get(slug=project),
		'sprint': Sprint.objects.get(pk=pk),
		'PBI': PBI.objects.filter(Q(project=Project.objects.get(slug=project)), Q(status='To Do') | Q(status='Unfinished')).exclude(sprint=Sprint.objects.get(pk=pk)),
	}
	if request.POST:
		for id in request.POST.getlist('PBIs'):
			selectedPBI = PBI.objects.get(pk=id)
			selectedPBI.sprint.add(Sprint.objects.get(pk=pk))
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
		Task.objects.filter(Q(PBI=PBI.objects.get(pk=pk)), Q(sprint=Sprint.objects.get(pk=sprint))).delete()
		tmp.save()
		return HttpResponseRedirect(reverse('sprint-home', kwargs={'project': project, 'sprint': sprint}))

	return render(request, 'sprintBacklog/removePBI.html', context)
