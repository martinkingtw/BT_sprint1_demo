from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import PBIs
from .forms import PBIForm

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

def delete(request):
	id = request.POST['id']
	PBIs.objects.get(pk=id).delete()
	context = {
		'dict': PBIs.objects.all().order_by('priority')
	}
	return render(request, 'productBacklog/home.html', context)

def create_pbi(request):
	form = PBIForm(request.POST or None)
	if form.is_valid():
		form.save()
		form = PBIForm()
		return home(request)

	context = {
		'form': form 
	}
	return render(request, 'productBacklog/create.html', context)
