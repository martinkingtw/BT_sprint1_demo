from django.shortcuts import render
from django.views.generic import (
	ListView, 
	CreateView, 
	DeleteView
)
from productBacklog.models import Project
from users.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail

class ProjectListView(ListView):
	model = Project
	template_name = 'project/home.html'
	context_object_name = 'projects'






class ProjectCreateView(CreateView):
	model = Project
	fields = [
		'title',
		'details',
		'duration',
	]
	template_name = 'project/project_form.html'

	def dispatch(self, request, *args, **kwargs):
		self.users = User.objects.all()
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['SM'] = self.users.filter(position=2)
		context['D'] = self.users.filter(position=3, project_id=None)
		return context


	def post(self, request, *args, **kwargs):
		info = request.POST
		print(info)
		if 'd' not in info:
			return HttpResponseRedirect(reverse('project-create'))
		emails = list()
		emails.append(info['sm'])
		for dev in info.getlist('d'):
			emails.append(dev)
		send_mail(
			'[Action Required] Join a project!',
			'Are you interested in joining ' + info['title'] + '? If it is the case, please click the following links!',
			'mkmuzha@gmail.com',
			emails,
		)
		return super(ProjectCreateView, self).post(request, *args, **kwargs)




class ProjectDeleteView(DeleteView):
	model = Project
	template_name = 'project/delete.html'
	slug_url_kwarg = 'project'
	def get_success_url(self):
		return '/'

	# def dispatch(self, request, *args, **kwargs):
	# 	self.project_id = kwargs['fk']
	# 	self.project = get_object_or_404(Project, pk=kwargs['fk'])
	# 	return super().dispatch(request, *args, **kwargs)

	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	context['project'] = self.project
	# 	return context