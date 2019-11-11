from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here......
class Project(models.Model):
	title = models.CharField(max_length=20, unique=True)
	details = models.TextField()
	slug = models.SlugField(unique=True, default="")
	duration = models.IntegerField("Sprint Duration(week)", default=2)
	
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('project-home')

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super().save(*args, **kwargs)
