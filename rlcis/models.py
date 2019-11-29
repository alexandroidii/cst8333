from django.db import models

# Create your models here.

class Incident(models.Model):
	country = models.CharField(max_length=60)
	region = models.CharField(max_length=60)
	bribed_by = models.CharField(max_length=100)
	bribed_by_other = models.CharField(max_length=100)
	bribe_type = models.CharField(max_length=60)
	bribe_type_other = models.CharField(max_length=60)
	location = models.CharField(max_length=60)
	first_occurence = models.DateTimeField('first occurence')
	resolution_date = models.DateTimeField('resolution date')
	reviewer = models.Foreignkey(Reviewer, on_delete=models.CASCADE)
	
class Reviewer(models.Model):
	first_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)
	employee_id = models.IntegerField()