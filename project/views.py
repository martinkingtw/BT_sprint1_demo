from django.shortcuts import render
from django.views.generic import (
	ListView, 
	CreateView, 
	DeleteView
)
from productBacklog.models import Project

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import User
from django.urls import reverse
from django.core.mail import send_mail

class ProjectListView(ListView):
	model = Project
	template_name = 'project/home.html'
	context_object_name = 'projects'






class ProjectCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
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

	def get_success_url(self):
		if 'd' not in self.info:
			self.object.delete()
			return reverse('project-create')
		msg = 'Are you interested in joining ' + self.info['title'] + '? If it is the case, please click the following links!\n'
		url = 'http://127.0.0.1:8000/' + 'join/' + str(self.object.pk) + '/' + self.info['sm']
		msg += url
		email = []
		email.append(User.objects.get(pk=int(self.info['sm'])).email)
		send_mail(
			'[Action Required] Join a project!',
			msg,
			'mkmuzha@gmail.com',
			email,
		)
		for dev in self.info.getlist('d'):
			email = []
			email.append(User.objects.get(pk=int(dev)).email)
			msg = 'Are you interested in joining ' + self.info[
				'title'] + '? If it is the case, please click the following links!\n'
			url = 'http://127.0.0.1:8000/' + 'join/' + str(self.object.pk) + '/' + dev
			msg += url
			send_mail(
				'[Action Required] Join a project!',
				msg,
				'mkmuzha@gmail.com',
				email,
			)
			return super(ProjectCreateView, self).get_success_url()

	def post(self, request, *args, **kwargs):
		self.info = request.POST
		return super(ProjectCreateView, self).post(request, *args, **kwargs)

	def test_func(self):
		if self.request.user.position == '3':
			return True
		return False


	




class ProjectDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Project
	template_name = 'project/delete.html'
	slug_url_kwarg = 'project'
	def get_success_url(self):
		return '/'

	def test_func(self):
		if self.request.user.position == '1':
			return True
		return False
	# def dispatch(self, request, *args, **kwargs):
	# 	self.project_id = kwargs['fk']
	# 	self.project = get_object_or_404(Project, pk=kwargs['fk'])
	# 	return super().dispatch(request, *args, **kwargs)

	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	context['project'] = self.project
	# 	return context


def join(request, project, user):
	context = {
		'project': Project.objects.get(pk=project),
	}
	joiner = User.objects.get(pk=user)
	joiner.project_id = Project.objects.get(pk=project)
	joiner.save()
	return render(request, 'project/join.html', context)
