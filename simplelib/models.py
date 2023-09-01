from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

''' 
	We create a custom user model as it is more flexible,
	and we can use custom validators
'''


class User(AbstractUser):
	username = models.CharField(
		max_length=30,
		unique=True
	)

	first_name = models.CharField(max_length=30, blank=False)
	last_name = models.CharField(max_length=30, blank=False)
	email = models.EmailField(unique=True, blank=False)
