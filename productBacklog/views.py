from django.shortcuts import render
from .models import PBIs
from .forms import PBIForm

def home(request):
	context = {
		'dict': PBIs.objects.all().order_by('priority')
	}
	return render(request, 'productBacklog/home.html', context)

def about(request):
	return render(request, 'productBacklog/about.html')

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