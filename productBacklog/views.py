from django.shortcuts import render
from django.views.generic import (
	ListView,
	DetailView, 
	CreateView, 
	DeleteView,
	UpdateView,
	)
from .models import PBIs, Project
from django.shortcuts import get_object_or_404

def home(request):
	context = {
		'dict': PBIs.objects.all().order_by('priority')
	}
	return render(request, 'productBacklog/home.html', context)

class PBListView(ListView):
	model = PBIs
	template_name = 'productBacklog/home.html'
	context_object_name = 'dict'
	def get_queryset(self):
		return PBIs.objects.filter(project_id=self.project_id)

	def dispatch(self, request, *args, **kwargs):
		self.project_id = kwargs['fk']
		self.project = get_object_or_404(Project, pk=kwargs['fk'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context

class PBDetailView(DetailView):
	model = PBIs
	template_name = 'productBacklog/detail.html'
	context_object_name = 'PBI'

	def dispatch(self, request, *args, **kwargs):
		self.project_id = kwargs['fk']
		self.project = get_object_or_404(Project, pk=kwargs['fk'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context

class PBCreateView(CreateView):
	model = PBIs
	# print(form.instance.project_id)
	fields = [
			'priority',
			'title',
			'status',
			'ESP',
			'details'
	]
	def dispatch(self, request, *args, **kwargs):
		self.project_id = kwargs['fk']
		self.project = get_object_or_404(Project, pk=kwargs['fk'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context

	def form_valid(self, form):
		form.instance.project = self.project
		return super().form_valid(form)

class PBUpdateView(UpdateView):
	model = PBIs
	# print(form.instance.project_id)
	fields = [
			'priority',
			'title',
			'status',
			'ESP',
			'details'
	]
	def dispatch(self, request, *args, **kwargs):
		self.project_id = kwargs['fk']
		self.project = get_object_or_404(Project, pk=kwargs['fk'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context


class PBDeleteView(DeleteView):
	model = PBIs
	template_name = 'productBacklog/delete.html'
	def get_success_url(self):
		return '/' + str(self.project_id) + '/product'

	def dispatch(self, request, *args, **kwargs):
		self.project_id = kwargs['fk']
		self.project = get_object_or_404(Project, pk=kwargs['fk'])
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


def delete(request, fk):
	id = request.POST['id']
	PBIs.objects.get(pk=id).delete()
	context = {
		'dict': PBIs.objects.all().order_by('priority')
	}
	return render(request, 'productBacklog/home.html', context)


