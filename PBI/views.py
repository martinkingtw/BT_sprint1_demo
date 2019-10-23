from django.shortcuts import render
from .models import PBIs

def home(request):
	context = {
		'dict': PBIs.objects.all() 
	}
	return render(request, 'PBI/home.html', context)

def about(request):
	return render(request, 'PBI/about.html')