from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import PBIs, Project
from django.shortcuts import get_object_or_404
# from .forms import PBIForm

def home(request):
	context = {
		'dict': PBIs.objects.all().order_by('priority')
	}
	return render(request, 'productBacklog/home.html', context)

class PBListView(ListView):
	model = PBIs
	template_name = 'productBacklog/home.html'
	context_object_name = 'dict'

	# def dispatch(self, request, *args, **kwargs):
	# 	self.project = get_object_or_404(Project)
	# 	return super().dispatch(request, *args, **kwargs)

	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	context['project_id'] = self.project.pk
	# 	print(context)
	# 	return context

class PBDetailView(DetailView):
	model = PBIs
	template_name = 'productBacklog/detail.html'
	context_object_name = 'PBI'

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
	# def dispatch(self, request, *args, **kwargs):
	# 	self.project = get_object_or_404(project)
	# 	return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		# form.instance.project_id = project.pk
		return super().form_valid(form)

class projectListView(ListView):
	model = Project
	template_name = 'productBacklog/project.html'

def about(request):
	return render(request, 'productBacklog/about.html')

def delete(request):
	id = request.POST['id']
	PBIs.objects.get(pk=id).delete()
	context = {
		'dict': PBIs.objects.all().order_by('priority')
	}
	return render(request, 'productBacklog/home.html', context)


