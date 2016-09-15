from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class School(models.Model):
	name = models.CharField(max_length=75)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=30)

class Address(models.Model):
	street_number = models.IntegerField()
	street_name = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=30)
	zipcode = models.IntegerField()
	description = models.CharField(max_length=300)
	address_2 = models.CharField(max_length=300)

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
	
class Category(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(max_length=500)

class Product(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(max_length=500)
	category = models.ForeignKey(Category)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	picture = models.ImageField()
	owner = models.ForeignKey(User)
	time_posted = models.DateTimeField(auto_now_add=True)
	time_updated = models.DateTimeField(auto_now=True)
	pick_up = models.CharField(max_length=50)

	OFF_MARKET = 'OM'
	FOR_SALE = 'FS'
	NEGOTIATING = 'N'
	SOLD = 'S'
	EXCHANGED = 'E'

	STATUS_CHOICES = (
		(OFF_MARKET, 'Off the market'),
		(FOR_SALE, 'For Sale'),
		(NEGOTIATING, 'Negotiating'),
		(SOLD, 'Sold'),
		(EXCHANGED, 'Exchanged'),
    )
	status = models.CharField(max_length=2,
    							choices=STATUS_CHOICES,
    							default=FOR_SALE)

	NEW = 'N'
	USED_GOOD = 'UG'
	USED_OKAY = 'UO'
	USED_POOR = 'UP'

	CONDITION_CHOICES = (
		(NEW, 'New condition'),
		(USED_GOOD, 'Used and in good condition'),
		(USED_OKAY, 'Used and in okay condition'),
		(USED_POOR, 'Used and in poor condition')
	)
	condition = models.CharField(max_length=2,
									choices=CONDITION_CHOICES,
									default=NEW)

