from django.db import models

class PBIs(models.Model):
	itemID = models.IntegerField()
	priority = models.IntegerField()
	title = models.CharField(max_length=10)
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
	ESP = models.IntegerField()
	details = models.TextField()

	def __str__(self):
		return self.title
