from django.shortcuts import render
from django.views.generic import (
	ListView,
	DetailView, 
	CreateView, 
	DeleteView,
	UpdateView,
	)
from .models import PBI, Project
from sprintBacklog.models import Task
from django.shortcuts import get_object_or_404
from datetime import timedelta, date

# def home(request):
# 	context = {
# 		'dict': PBI.objects.all().order_by('priority')
# 	}
# 	return render(request, 'productBacklog/home.html', context)

class PBListView(ListView):
	model = PBI
	template_name = 'productBacklog/home.html'

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		PBIs = []
		for pbi in PBI.objects.filter(project_id=self.project).order_by('priority'):
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
		queryset = PBI.objects.filter(project_id=self.project).order_by('priority')
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

class PBCreateView(CreateView):
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
		return super().form_valid(form)

	def post(self, request, *args, **kwargs):
		queryset = PBI.objects.filter(project_id=self.project).order_by('priority')
		prioirity = request.POST['priority']
		for obj in queryset:
			if obj.priority >= int(prioirity):
				obj.priority += 1
				obj.save()
		return super(PBCreateView, self).post(request)

class PBUpdateView(UpdateView):
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
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context


	def post(self, request, *args, **kwargs):
		queryset = PBI.objects.filter(project_id=self.project).order_by('priority')
		prioirity = request.POST['priority']
		for obj in queryset:
			if obj.priority >= int(prioirity) and obj != self.object:
				obj.priority += 1
				obj.save()
		return super(PBUpdateView, self).post(request)




class PBDeleteView(DeleteView):
	model = PBI
	template_name = 'productBacklog/delete.html'
	def get_success_url(self):
		return '/' + str(self.project.slug) + '-product'

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context

class projectListView(ListView):
	model = Project
	template_name = 'productBacklog/project.html'

def about(request):
	return render(request, 'productBacklog/about.html')


def delete(request):
	id = request.POST['id']
	PBI.objects.get(pk=id).delete()
	context = {
		'dict': PBI.objects.all().order_by('priority')
	}
	return render(request, 'productBacklog/home.html', context)


