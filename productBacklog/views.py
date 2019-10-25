from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import PBIs

def home(request):
	context = {
		'dict': PBIs.objects.all().order_by('priority')
	}
	return render(request, 'productBacklog/home.html', context)

class PBListView(ListView):
	model = PBIs
	template_name = 'productBacklog/home.html'
	context_object_name = 'dict'


class PBDetailView(DetailView):
	model = PBIs
	template_name = 'productBacklog/detail.html'
	context_object_name = 'PBI'

def about(request):
	return render(request, 'productBacklog/about.html')