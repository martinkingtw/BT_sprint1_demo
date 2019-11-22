from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import (
	ListView, 
	CreateView, 
	DeleteView
)
from productBacklog.models import Project

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.utils.text import slugify

class ProjectListView(ListView):
	model = Project
	template_name = 'project/home.html'
	context_object_name = 'projects'



def redirect_to_home(request):

	if request.user.position == '2':
		return HttpResponseRedirect(reverse('project-home'))
	elif request.user.project.first():
		return HttpResponseRedirect(reverse('productBacklog-home',kwargs={'project': slugify(request.user.project.first().title)}))

	else:
		return HttpResponseRedirect(reverse('project-home'))


	
		

class ProjectCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
	model = Project
	fields = [
		'title',
		'details',
	]
	template_name = 'project/project_form.html'

	def dispatch(self, request, *args, **kwargs):
		self.self = request.user
		self.users = User.objects.all()
		self.url = request.get_full_path()
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.url == '/duplicate/':
			context['duplicate'] = 'True'
		else:
			context['duplicate'] = 'False'
		context['SM'] = self.users.filter(position=2)
		context['D'] = self.users.filter(position=3, project=None).exclude(pk=self.self.pk)
		return context

	def get_success_url(self):
		if 'd' not in self.info:
			self.object.delete()
			return reverse('project-create')
		self.self.position = 1
		self.self.project.add(Project.objects.get(pk=self.object.pk))
		self.self.save()
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
		try:
			Project.objects.get(title=self.info['title'])
			return redirect(reverse('project-duplicate'))
		except:
			return super(ProjectCreateView, self).post(request, *args, **kwargs)

	def test_func(self):
		if self.request.user.position == '3':
			return True
		return False


	




class ProjectDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Project
	template_name = 'project/delete.html'
	slug_url_kwarg = 'project'

	def test_func(self):
		if self.request.user.position == '1':
			return True
		return False

	def dispatch(self, request, *args, **kwargs):
		self.self = request.user
		return super().dispatch(request, *args, **kwargs)

	def get_success_url(self):
		self.self.position = 3
		self.self.save()
		return '/'

	# def dispatch(self, request, *args, **kwargs):
	# 	self.project_id = kwargs['fk']
	# 	self.project = get_object_or_404(Project, pk=kwargs['fk'])
	# 	return super().dispatch(request, *args, **kwargs)

	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	context['project'] = self.project
	# 	return context


@login_required
def join(request, project, user):
	if request.user.pk != user:
		return render(request, 'project/noPermit.html', {})
	try:
		context = {
			'project': Project.objects.get(pk=project),
		}
	except:
		return render(request, 'project/noProject.html', {})
	joiner = User.objects.get(pk=user)
	if joiner.position == '2':
		joiner.project.add(Project.objects.get(pk=project))
	elif not joiner.project.exists():
		joiner.project.add(Project.objects.get(pk=project))
	else:
		return render(request, 'project/noPermit.html', {})
	joiner.save()
	return render(request, 'project/join.html', context)

