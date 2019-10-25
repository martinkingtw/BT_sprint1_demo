from django.shortcuts import render
from .models import PBIs

def home(request):
	context = {
		'dict': PBIs.objects.all().order_by('priority')
	}
	return render(request, 'productBacklog/home.html', context)

def about(request):
	return render(request, 'productBacklog/about.html')

def delete(request):
	id = request.POST['id']
	PBIs.objects.get(pk=id).delete()
	context = {
		'dict': PBIs.objects.all().order_by('priority')
	}
	return render(request, 'productBacklog/home.html', context)