from django.db import models

class PBIs(models.Model):
    itemID = models.IntegerField()
    priority = models.IntegerField()
    title = models.CharField(max_length=10)
    status = models.IntegerField()
    ESP = models.IntegerField()
    details = models.TextField()
    
    def __str__(self):
    	return self.title
