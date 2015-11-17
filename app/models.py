from django.db import models
# Create your models here.
from django.contrib.auth.models import User

class GitHubUser(models.Model):
	user = models.ForeignKey(User)
	access_token = models.CharField(max_length=50)
	
	class Meta:
		unique_together = ('user', 'access_token')

	def __str__(self):
		return self.user.email

class Create_repo(models.Model):
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=1000)

	def __str__(self):
		return self.name