from django.db import models
from django.urls import reverse
from project.models import Project
#comment
class PBI(models.Model):
	priority = models.IntegerField()
	title = models.CharField(max_length=20)
	status_choice = [
		('To Do', 'To Do'),
		('Doing', 'Doing'),
		('Done', 'Done'),
	]
	status = models.CharField(
		max_length = 5,
		choices = status_choice,
		default = 'To Do',
	)
	ESP = models.IntegerField()
	details = models.TextField()
	project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True, default=None)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('productBacklog-home', kwargs={'project': self.project.slug})

	def save(self, *args, **kwargs):
		# adjust priority here
		super().save(*args, **kwargs)