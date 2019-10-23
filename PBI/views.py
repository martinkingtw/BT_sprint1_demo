from django.shortcuts import render
from .models import PBIs

dict = [
	{
		'id':'1',
		'title':'PBI1'

	},
	{
		'id':'2',
		'title':'PBI2'

	}
]

def home(request):
	context = {
		'dict': PBIs.objects.all() 
	}
	return render(request, 'PBI/home.html', context)

def about(request):
	return render(request, 'PBI/about.html')