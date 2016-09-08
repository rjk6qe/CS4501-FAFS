from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class School(models.Model):
	name = models.CharField(max_length=75)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=30)

class UserManager(BaseUserManager):

	def create_user(self, email, school, password=None):
		if not (email and school):
			raise ValueError("Need an email!")
		
		u = self.model(
			email=UserManager.normalize_email(email),
			school_id = school,
			)
		u.set_password(password)
		u.save()
		return u

	def create_superuser(self, email, password=None):
		u = self.create_user(email, password)
		u.is_superuser = True
		u.save()
		return u

class User(AbstractBaseUser):
	school_id = models.ForeignKey(School)
	email = models.EmailField(unique=True, blank=False)
	rating = models.IntegerField(blank=True, null=True)
	phone_number = models.CharField(max_length=20, blank=True)
	objects = UserManager()

	USERNAME_FIELD = 'email'
	


