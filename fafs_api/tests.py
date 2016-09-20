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

class test_superuser(TestCase):

	bad_school_values = {"name":"Virginia Tech", "city":"Blacksburg", "state":"Virginia"}
	good_school_values = {"name":"University of Virginia", "city":"Charlottesville", "state":"Virginia"}
	user_one_values = {"email":"email@email.com", "password":"password2","school_id":1}

	def create_school(self,dictionary):
		School.objects.create(
			name=dictionary['name'],
			city=dictionary['city'],
			state=dictionary['state']
			)

	def setUp(self):
		self.create_school(self.bad_school_values)

	def test_create_superuser(self):
		s = School.objects.get(name=self.bad_school_values['name'])
		s_pk = s.pk
		
		u = User.objects.create_superuser(
			email=self.user_one_values['email'],
			password=self.user_one_values['password'],
			school=s_pk)

		self.assertEqual(
			u.is_superuser,
			True,
			"Created user is not a superuser"
			)

class test_patch_user(TestCase):


	bad_school_values = {"name":"Virginia Tech", "city":"Blacksburg", "state":"Virginia"}
	good_school_values = {"name":"University of Virginia", "city":"Charlottesville", "state":"Virginia"}
	user_one_values = {"email":"email@email.com", "password":"password2","school_id":1}

	def create_school(self,dictionary):
		School.objects.create(
			name=dictionary['name'],
			city=dictionary['city'],
			state=dictionary['state']
			)

	def setUp(self):
		self.create_school(self.bad_school_values)
		User.objects.create_user(
			email=self.user_one_values['email'],
			password=self.user_one_values['password'],
			school=self.user_one_values['school_id']
			)

	def test_update_user(self):
		updated_user = User.objects.get(email=self.user_one_values['email'])
		new_email = 'new_email@new_email.com'
		new_password = 'new_password'
		response = self.client.patch(
			'/api/users/',
			data=json.dumps({
				"user_pk":updated_user.pk,
				"email":new_email,
				"password": new_password}),
			content_type="application/json"
			)
		self.assertEqual(
			response.status_code,
			200,
			"Incorrect status code for valid update"
			)
		new_user = User.objects.get(email=new_email)

		self.assertEqual(
			new_user.pk,
			updated_user.pk,
			"Primary key changed"
			)
		self.assertEqual(
			new_user.email,
			new_email,
			"Email was not changed"
			)

		auth_user = authenticate(username=new_user.email, password=new_password)
		self.assertNotEqual(
			auth_user,
			None,
			"User was not found when authenticating"
			)

	def test_bad_update_user(self):
		updated_user = User.objects.get(email=self.user_one_values['email'])
		new_email = 'new_email@new_email.com'
		new_password = 'new_password'
		response = self.client.patch(
			'/api/users/',
			data=json.dumps({
				"user_pk": 65,
				"email":new_email,
				"password": new_password
				}),
			content_type="application/json"
			)
		self.assertEqual(
			response.status_code,
			400,
			"Incorrect response code for bad update"
			)

