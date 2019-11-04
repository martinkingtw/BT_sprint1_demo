from django.shortcuts import render
from django.views.generic import (
	ListView,
	DetailView, 
	CreateView, 
	DeleteView,
	UpdateView,
	)
from .models import PBI, Project
from django.shortcuts import get_object_or_404

# def home(request):
# 	context = {
# 		'dict': PBI.objects.all().order_by('priority')
# 	}
# 	return render(request, 'productBacklog/home.html', context)

class PBListView(ListView):
	model = PBI
	template_name = 'productBacklog/home.html'
	context_object_name = 'dict'
	ordering = ['priority']

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context

	def get_queryset(self):
		queryset = PBI.objects.filter(project_id=self.project).order_by('priority')
		numOfPBI = len(queryset)
		index = 0
		for obj in queryset:
			if obj.priority == index:
				obj.priority -= 1
				obj.save()
			elif obj.priority > numOfPBI:
				obj.priority = numOfPBI
				obj.save()
			else:
				index = obj.priority
		index = 1
		queryset = PBI.objects.filter(project_id=self.project).order_by('priority')
		for obj in queryset:
			obj.priority = index
			index = index + 1
			obj.save()
		return queryset

class PBDetailView(DetailView):
	model = PBI
	template_name = 'productBacklog/detail.html'
	context_object_name = 'PBI'

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context

class PBCreateView(CreateView):
	model = PBI
	fields = [
			'priority',
			'title',
			'ESP',
			'details'
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

class PBUpdateView(UpdateView):
	model = PBI
	fields = [
			'priority',
			'title',
			'status',
			'ESP',
			'details'
	]

	def dispatch(self, request, *args, **kwargs):
		self.project = get_object_or_404(Project, slug=kwargs['project'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project'] = self.project
		return context


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


def delete(request, fk):
	id = request.POST['id']
	PBI.objects.get(pk=id).delete()
	context = {
		'dict': PBI.objects.all().order_by('priority')
	}
	return render(request, 'productBacklog/home.html', context)


