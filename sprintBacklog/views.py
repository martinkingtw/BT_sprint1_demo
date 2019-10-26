from django.shortcuts import render

# Create your views here.
def home(request):
	tmp = {"tmp" : 'tmp'}
	context = {
		'dict': tmp,
		'project_id': 8
	}
	return render(request, 'SprintBacklog/home.html', context)