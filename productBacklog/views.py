from django.shortcuts import render
from django.views.generic import (
	ListView,
	DetailView, 
	CreateView, 
	DeleteView,
	UpdateView,
	)
from django.db.models import Q

from .models import PBI, Project
from sprintBacklog.models import Task
from django.shortcuts import get_object_or_404
from datetime import timedelta, date
from users.models import Profile

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

# def home(request):
# 	context = {
# 		'dict': PBI.objects.all().order_by('priority')
# 	}
# 	return render(request, 'productBacklog/home.html', context)
class AllPBListView(ListView):
	model = PBI
	template_name = 'productBacklog/home_2.html'

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		# sprint number
		PBIs = []
		done = PBI.objects.filter(Q(project=self.project), Q(status="Done"))
		queryset = PBI.objects.filter(Q(project=self.project), Q(status="Doing") | Q(status="To Do") | Q(status="Unfinished")).order_by('priority')
		for pbi in list(done) + list(queryset):
			n = ''
			for i in pbi.sprint.all():
				n += i.title[-1]
				n += ", "
			if n == "":
				n = "N/A.."
			tmp = {"pbi": pbi,
				   "sprint_number": n[:-2]
				   }
			PBIs.append(tmp)
		context['PBIs'] = PBIs
		return context

	def get_queryset(self):
		index = 1
		queryset = PBI.objects.filter(Q(project=self.project), Q(status="Doing") | Q(status="To Do") | Q(status="Unfinished")).order_by('priority')
		for obj in queryset:
			obj.priority = index
			index = index + 1
			obj.save()
		return queryset

class TodoPBListView(ListView):
	model = PBI
	template_name = 'productBacklog/home_1.html'

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		# sprint number, accumulative ESP
		PBIs = []
		accumulative = 0
		for pbi in PBI.objects.filter(Q(project=self.project), Q(status="Doing") | Q(status="To Do") | Q(status="Unfinished")).order_by('priority'):
			n = ''
			for i in pbi.sprint.all():
				n += i.title[-1]
				n += ", "
			if n == "":
				n = "N/A.."

			accumulative += pbi.ESP
			tmp = {"pbi": pbi,
				   "acc_SP": accumulative,
				   "sprint_number": n[:-2]
				   }
			PBIs.append(tmp)
		context['PBIs'] = PBIs
		return context

	def get_queryset(self):
		queryset = PBI.objects.filter(Q(project=self.project), Q(status="Doing") | Q(status="To Do") | Q(status="Unfinished")).order_by('priority')
		index = 1
		for obj in queryset:
			obj.priority = index
			index = index + 1
			obj.save()
		return queryset

class PBDetailView(DetailView):
	model = PBI
	template_name = 'productBacklog/detail.html'

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		self.pbi = get_object_or_404(PBI, pk=kwargs['pk'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		context['editable'] = self.pbi.editable()
		n = ''
		for i in self.pbi.sprint.all():
			n += i.title[-1]
			n += ", "
		if n == "":
			n = "N/A.."
		tmp = {"pbi": self.pbi,
			   "sprint_number": n[:-2]
			   }
		context['PBI'] = tmp
		return context

class PBCreateView(UserPassesTestMixin,CreateView):
	model = PBI
	fields = [
			'priority',
			'title',
			'ESP',
			'details',
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
		# priority
		queryset = PBI.objects.filter(Q(project=self.project), Q(status="Doing") | Q(status="To Do") | Q(status="Unfinished")).order_by('priority')
		prioirity = form.instance.priority
		for obj in queryset:
			if obj.priority >= int(prioirity):
				obj.priority += 1
				obj.save()
		return super().form_valid(form)

	def post(self, request, *args, **kwargs):
		return super(PBCreateView, self).post(request)

	def test_func(self):
		if self.request.user.position == '1':
			return True
		return False


class PBUpdateView(UserPassesTestMixin,UpdateView):
	model = PBI
	fields = [
			'priority',
			'title',
			'ESP',
			'details',
			'status'
	]

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		self.object = self.get_object()
		self.OGpriority = self.object.priority
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context

	def form_valid(self, form):
		prioirity = form.instance.priority
		queryset = PBI.objects.filter(Q(project=self.project), Q(status="Doing") | Q(status="To Do") | Q(status="Unfinished")).order_by('priority')
		firstRun = True
		for obj in queryset:
			if obj.priority >= int(prioirity) and obj != self.object:
				if firstRun and self.object.priority > self.OGpriority:
					obj.priority -= 2
					firstRun = False
				obj.priority += 1
				obj.save()
		return super().form_valid(form)

	def post(self, request, *args, **kwargs):
		return super(PBUpdateView, self).post(request)

	def test_func(self):
		pbi = self.get_object()
		if self.request.user.position == '1':
			return True
		return False


class PBDeleteView(UserPassesTestMixin,DeleteView):
	model = PBI
	template_name = 'productBacklog/delete.html'
	def get_success_url(self):
		return '/' + str(self.project.slug) + '/unfinished'

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context

	def test_func(self):
		pbi = self.get_object()
		if self.request.user.position == '1':
			return True
		return False

class projectListView(ListView):
	model = Project
	template_name = 'productBacklog/project.html'


