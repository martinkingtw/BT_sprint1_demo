from django.db import models
from django.urls import reverse

# Create your models here.
class Project(models.Model):
	title = models.CharField(max_length=20, unique=True)
	details = models.TextField()
	
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('project-home')