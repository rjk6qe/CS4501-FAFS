from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError

import os
import hmac
from django.conf import settings

class School(models.Model):
	name = models.CharField(max_length=75, unique=True)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=30)

	def clean(self):
		if not (self.name and self.city and self.state):
			raise ValidationError({
				"Error":"Missing required fields"
				})
		try:
			School.objects.get(name=self.name)
			raise ValidationError({
				"Error":"This school already exists"
				})
		except School.DoesNotExist:
			pass

class Address(models.Model):
	street_number = models.IntegerField()
	street_name = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=30)
	zipcode = models.IntegerField()
	description = models.CharField(max_length=300)
	address_2 = models.CharField(max_length=300)

class UserManager(BaseUserManager):

	def clean_school(self, school_id):
		try:
			s = School.objects.get(pk=school_id)
			return s
		except School.DoesNotExist:
			raise ValidationError({
				"Error":"Invalid school primary key."
				})

	def clean_email(self, email):
		try:
			User.objects.get(email=email)
			raise ValidationError({
				"Error":"User with this email already exists"
				})
		except User.DoesNotExist:
			return email

	def create_user(self, email=None, school=None, password=None):
		u = self.model(
			email=UserManager.normalize_email(email),
			school_id=self.clean_school(school)
			)
		u.set_password(password)
		u.clean()
		u.save()
		return u

	def create_superuser(self, email=None, password=None, school=None):
		u = self.create_user(email=email, password=password, school=school)
		u.is_superuser = True
		u.save()
		return u

	def update_user(self, user_pk, email=None, password=None):
		try:
			user = User.objects.get(pk=user_pk)
			change = False
			if email:
				user.email = self.clean_email(email)
				change = True
			if password:
				user.set_password(password)
				change = True
			if change:
				user.save()
				return user
			else:
				raise ValidationError({
					"Error":"Must specify new email or password"
					})
		except User.DoesNotExist:
			raise ValidationError({
				"Error":"Invalid user id" + str(user_pk)
				})

class User(AbstractBaseUser):
	school_id = models.ForeignKey(School)
	email = models.EmailField(unique=True, blank=False)
	rating = models.IntegerField(blank=True, null=True)
	phone_number = models.CharField(max_length=20, blank=True)

	objects = UserManager()

	USERNAME_FIELD = 'email'

	def clean(self):
		if not (self.email and self.school_id and self.password):
			raise ValidationError(
				{"Error":"Missing required fields."}
				)
		try:
			User.objects.get(email=self.email)
			raise ValidationError(
				{"Error":"User with this email already exists"}
				)
		except User.DoesNotExist:
			pass #this is desired

def get_authenticator_token():
	while True:
		authenticator = hmac.new(key = settings.SECRET_KEY.encode('utf-8'), msg = os.urandom(32), digestmod = 'sha256').hexdigest()
		try:
			dup_test = Authenticator.objects.get(token=authenticator)
		except Authenticator.DoesNotExist:
			dup_test = None
		if dup_test is None:
			break

	return authenticator

class Authenticator(models.Model):
	token = models.CharField(max_length=255,
							primary_key=True,
							default=get_authenticator_token)
	email = models.ForeignKey(User)
	date_created = models.DateField(auto_now_add=True)

class Category(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(max_length=500)

class Product(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(max_length=500)
	category_id = models.ForeignKey(Category)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	#picture = models.ImageField()
	owner_id = models.ForeignKey(User)
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


class Transaction(models.Model):
	seller = models.ForeignKey(User, related_name='transaction_seller')
	buyer = models.ForeignKey(User, related_name='transaction_buyer')
	product_id = models.ForeignKey(Product)
