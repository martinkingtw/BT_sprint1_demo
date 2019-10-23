from django.shortcuts import render

# Create your views here.
def home(request):
	tmp = {"tmp" : 'tmp'}
	context = {
		'dict': tmp
	}
	return render(request, 'SprintBacklog/home.html', context)