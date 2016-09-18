from django.test import TestCase
from django.contrib.auth import authenticate
from fafs_api.models import User, School, UserManager

import json

# Create your tests here.

class test_user_creation(TestCase):

	init_school_values = {"name":"University of Virginia", "city":"Charlottesville", "state":"Virginia"}
	init_user_values = {"email":"gmail@gmail.com", "password":"password1"}
	user_one_values = {"email":"email@email.com", "password":"password2","school_id":1}

	def create_school(self,dictionary):
		return School.objects.create(
			name=dictionary['name'],
			city=dictionary['city'],
			state=dictionary['state']
			)

	def create_user(self, dictionary, school):
		return User.objects.create_user(
			email=dictionary['email'],
			password=dictionary['password'],
			school=school.pk
			)

	def setUp(self):
		school = self.create_school(self.init_school_values)
		self.create_user(self.init_user_values, school)

	def test_get_created_users(self):
		response = self.client.get('/api/users/')
		self.assertEqual(
			len(json.loads(response.content.decode('utf-8'))),
			1,
			"Incorrect number of users shown after setup"
			)
		self.assertEqual(
			len(User.objects.all()),
			1,
			"Incorrect number of users in database"
			)

	def test_create_user_with_non_unique_email(self):
		response = self.client.post(
			'/api/users/',
			data=json.dumps(self.init_user_values),
			content_type="application/json"
			)
		self.assertEqual(
			response.status_code,
			400,
			"Incorrect response code")
		self.assertEqual(
			len(User.objects.all()),
			1,
			"Incorrect  number of users in database after unsuccessfull user request"
			)

	def test_create_user_with_unique_email(self):
		response = self.client.post(
			'/api/users/',
			data=json.dumps(self.user_one_values),
			content_type="application/json"
			)
		self.assertEqual(
			response.status_code,
			200,
			"Incorrect response code")
		self.assertEqual(
			len(User.objects.all()),
			2,
			"Incorrect number of users in db after successfull user creation")
		
		response = json.loads(response.content.decode('utf-8'))
		user_email = response['email']
		
		self.assertEqual(
			user_email,
			self.user_one_values['email'],
			"Incorrect email"
			)

class test_school_creation(TestCase):
	bad_school_values = {"name":"Virginia Tech", "city":"Blacksburg", "state":"Virginia"}
	good_school_values = {"name":"University of Virginia", "city":"Charlottesville", "state":"Virginia"}

	def create_school(self,dictionary):
		School.objects.create(
			name=dictionary['name'],
			city=dictionary['city'],
			state=dictionary['state']
			)

	def setUp(self):
		self.create_school(self.bad_school_values)

	def test_create_non_unique_school(self):
		response = self.client.post(
			'/api/schools/',
			data=json.dumps(self.bad_school_values),
			content_type="application/json"
			)
		self.assertEqual(
			response.status_code,
			400,
			"Incorrect response code")
		self.assertEqual(
			len(School.objects.all()),
			1,
			"Incorrect number of schools in database after unsuccessfull creation request"
			)

	def test_create_unique_school(self):
		response = self.client.post(
			'/api/schools/',
			data=json.dumps(self.good_school_values),
			content_type="application/json"
			)
		self.assertEqual(
			len(School.objects.all()),
			2,
			"Incorrect number of schools in db after successfull school creation")
		self.assertEqual(
			response.status_code,
			200,
			"Incorrect response code")
