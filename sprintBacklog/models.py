from django.db import models
from django.urls import reverse
from project.models import Project
from users.models import User
from datetime import date
from django.db.models import Q

class Sprint(models.Model):
	title = models.CharField(max_length=20, default="Sprint")
	available_effort = models.IntegerField()
	start_date = models.DateField(blank=True, null=True)
	details = models.TextField(null=True)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True, default=None)
	
	status_choice = [
		('Not Started', 'Not Started'),
		('Started', 'Started'),
		('Ended', 'Ended'),
	]
	status = models.CharField(
		max_length = 20,
		choices = status_choice,
		default ='Not Started',
	)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('sprint-home', kwargs={'project': self.project.slug, 'sprint': self.pk})

	def save(self, *args, **kwargs):
		number_of_sprint = Sprint.objects.filter(project=self.project).count()
		if Sprint.objects.filter(project=self.project).count() == None:
			number_of_sprint = 1
		else:
			number_of_sprint += 1

		if self not in Sprint.objects.filter(project=self.project):
			self.title = "Sprint" + str(number_of_sprint)
		super().save(*args, **kwargs)

	def editable(self):
		return self.status == 'Not Started'

	def startSprint(self):
		self.status = 'Started'
		self.start_date = date.today()
		self.save()
		for i in PBI.objects.filter(sprint=self):
			i.status = "Doing"
			i.start_date = date.today()
			i.save()

	def endSprint(self):
		self.status = 'Ended'
		self.save()
		queryset = Sprint.objects.filter(project=self.project).order_by('pk')
		count = 0
		unfinished = []
		for obj in PBI.objects.filter(sprint=self):
			todo = Task.objects.filter(status='To Do', PBI=obj, sprint=self)
			doing = Task.objects.filter(status='Doing', PBI=obj, sprint=self)
			done = Task.objects.filter(status='Done', PBI=obj, sprint=self)

			if todo or doing:
				# count number of unfinished in order to adjust the priority
				unfinished.append(obj)
				count += 1
			elif not todo and not doing:
				obj.status = 'Done'
				obj.save()

		# setting priority
		for i in PBI.objects.filter(Q(project=self.project), Q(status="Doing") | Q(status="To Do") | Q(status="Unfinished")).order_by('priority'):
			i.priority += count
			i.save()
		count = 1
		for i in unfinished:
			i.priority = count
			i.status = "Unfinished"
			count += 1
			i.save()

from productBacklog.models import PBI

class Task(models.Model):
	title = models.CharField(max_length=20, default="Task")
	status_choice = [
		('To Do', 'To Do'),
		('Doing', 'Doing'),
		('Done', 'Done'),
	]
	status = models.CharField(
		max_length = 5,
		choices = status_choice,
		default ='To Do',
	)
	effort = models.IntegerField("effort(hour)")
	details = models.TextField(null=True)
	sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, default=None)
	PBI = models.ForeignKey(PBI, on_delete=models.CASCADE, default=None)
	task_owner = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('sprint-home', kwargs={'project': self.sprint.project.slug, 'sprint': self.sprint.pk})

	def save(self, *args, **kwargs):
		# adjust priority here
		super().save(*args, **kwargs)

	def editable(self):
		return not self.sprint.status == 'Ended'