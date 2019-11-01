from django.db import models
from django.urls import reverse
from project.models import Project
from productBacklog.models import PBI
from django.contrib.auth.models import User

class Sprint(models.Model):
	title = models.CharField(max_length=20, default="Sprint")
	available_effort = models.IntegerField()
	start_date = models.DateField(default="date.today")
	duration = models.IntegerField("duration(week)", default=2)
	details = models.TextField(null=True)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True, default=None)

	def __str__(self):
		return self.title

	# def get_absolute_url(self):
		# return reverse('sprint-home', kwargs={'project': self.project.slug, 'sprint': self.pk})

	def save(self, *args, **kwargs):
		# adjust priority here
		super().save(*args, **kwargs)

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

	# def get_absolute_url(self):
		# return reverse('sprint-home', kwargs={'project': self.project.slug, 'sprint': self.pk})

	def save(self, *args, **kwargs):
		# adjust priority here
		super().save(*args, **kwargs)