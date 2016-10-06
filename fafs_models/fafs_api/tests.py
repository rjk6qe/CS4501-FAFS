from django.test import TestCase
from django.contrib.auth import authenticate
from fafs_api.models import User, School, UserManager
from fafs_api.admin import authenticate

import json

# Create your tests here.

def json_response_to_dict(response):
	return response.json()


def post_request(client, url, data):
	status = True
	if isinstance(data, list):
		num_objs = len(data)
		for i in range(0, num_objs):
			obj = data[i]
			response = json_response_to_dict(
				client.post(
					url,
					data=json.dumps(obj),
					content_type="application/json"
					)
				)
			status = status and response['status']
		return status
	elif isinstance(data, dict):
		return client.post(
			url,
			data=json.dumps(data),
			content_type="application/json"
			)
	else:
		return None

def get_request(client, url, pk=None):
	get_url = url
	if pk is not None:
		get_url = get_url + str(pk) + '/'
	return client.get(
		get_url
		)

def patch_request(client, url, data):
	return client.patch(
		url,
		data=json.dumps(data),
		content_type="application/json"
		)

def delete_request(client, url, pk=None):
	delete_url = url
	if pk is not None:
		delete_url = delete_url + str(pk) + '/'
	return client.delete(
		delete_url
		)

def create_model(model, data):
	if model == School:
		School.objects.create(
			name=data['name'],
			city=data['city'],
			state=data['state']
			)

class test_user(TestCase):

	school_values = {"name":"University of Virginia", "city":"Charlottesville", "state":"Virginia"}
	user_list = [
		{"email":"gmail@gmail.com", "password":"password1","school_id":"1"},
		{"email":"email@email.com", "password":"password2","school_id":"1"}
		]
	required_models = [School,]
	required_model_fields = {str(School):school_values}
	url = "/api/v1/users/"

	def setUp(self):
		for model in self.required_models:
			create_model(model, self.required_model_fields[str(model)])

	def test_create_user(self):
		user = self.user_list[0]
		response = json_response_to_dict(
			post_request(
				self.client,
				self.url,
				data=user
				)
			)
		self.assertEqual(
			response['status'],
			True,
			"Incorrect response for valid user data"
			)
		self.assertEqual(
			response['response']['email'],
			user['email'],
			"Incorrect email"
			)

	def test_create_user_with_nonunique_email(self):
		user = self.user_list[0]
		post_request(
			self.client,
			self.url,
			user
			)
		response = json_response_to_dict(
			post_request(
				self.client,
				self.url,
				user,
				)
			)
		self.assertEqual(
			response['status'],
			False,
			"Incorrect response for invalid user data")

	def test_get_user_by_id(self):
		user = self.user_list[0]
		response = json_response_to_dict(
			post_request(
				self.client,
				self.url,
				user
				)
			)
		user_id = response['response']['pk']
		response = json_response_to_dict(
			get_request(
				self.client,
				self.url,
				pk=user_id
				)
			)
		self.assertEqual(
			response['status'],
			True,
			"Incorrect response for valid user id"
			)
		self.assertEqual(
			response['response']['email'],
			user['email'],
			"Retrieved incorrect email for user"
			)

	def test_get_user_with_incorrect_id(self):
		user = self.user_list[0]
		response = json_response_to_dict(
			post_request(
				self.client,
				self.url,
				user,
				)
			)
		user_id = response['response']['pk']
		response = json_response_to_dict(
			get_request(
				self.client,
				self.url,
				pk=13
				)
			)
		self.assertEqual(
			response['status'],
			False,
			"Incorrect response for invalid GET request"
			)

	def test_get_multiple_users(self):
		num_users = len(self.user_list)
		post_request(
			self.client,
			self.url,
			self.user_list
			)
		response = json_response_to_dict(
			get_request(
				self.client,
				self.url
				)
			)
		self.assertEqual(
			len(response['response']),
			num_users,
			"Incorrect number of users returned"
			)

	def test_update_user_with_valid_email(self):
		user = self.user_list[0]
		response = json_response_to_dict(
			post_request(
				self.client,
				self.url,
				user
				)
			)
		user_obj = User.objects.get(email=user['email'])

		user_id = response['response']['pk']
		response = json_response_to_dict(
			patch_request(
				self.client,
				self.url,
				{"user_pk":user_id,
				"email":self.user_list[1]['email'],
				"password":self.user_list[1]['password']}
				)
			)
		self.assertEqual(
			response['status'],
			True,
			"Incorrect status when updating a user with a valid email"
			)

		auth_user = authenticate(
			username=self.user_list[1]['email'],
			password=self.user_list[1]['password']
			)
		self.assertEqual(
			user_obj,
			auth_user,
			"Login failed after updating user object"
			)

	def test_update_user_with_invalid_email(self):
		num_users = len(self.user_list)
		post_request(
			self.client,
			self.url,
			self.user_list
			)
		response = json_response_to_dict(
			patch_request(
				self.client,
				self.url,
				{"pk":0, "email":self.user_list[1]['email'], "password":self.user_list[1]['password']},
				)
			)
		self.assertEqual(
			response['status'],
			False,
			"Incorrect status when updating a user with an email that was already taken"
			)

	def test_delete_user_with_valid_key(self):
		user = self.user_list[0]
		response = json_response_to_dict(
			post_request(
				self.client,
				self.url,
				user
				)
			)
		user_obj = User.objects.get(email=user['email'])
		response = json_response_to_dict(
			delete_request(
				self.client,
				self.url,
				pk=user_obj.pk
				)
			)
		self.assertEqual(
			response['status'],
			True,
			"Incorrect status after delete call on valid id"
			)
		self.assertEqual(
			len(User.objects.all()),
			0,
			"Incorrect number of users after deletion"
			)
		self.assertEqual(
			authenticate(username=user['email'],password=user['password']),
			None,
			"User was able to login with deleted credentials"
			)

	def test_delete_user_with_invalid_key(self):
		user = self.user_list[0]
		response = json_response_to_dict(
			post_request(
				self.client,
				self.url,
				user,
				)
			)
		user_obj = User.objects.get(email=user['email'])
		response = json_response_to_dict(
			delete_request(
				self.client,
				self.url,
				342
				)
			)
		self.assertEqual(
			response['status'],
			False,
			"Incorrect status after delete call on invalid id"
			)
		self.assertEqual(
			len(User.objects.all()),
			1,
			"Incorrect number of users after failed deletion"
			)
		self.assertEqual(
			authenticate(username=user['email'],password=user['password']),
			user_obj,
			"User was unable to login after failed deletion"
			)

class test_school(TestCase):

	school_list = [
		{"name":"That other school", "city":"Blacksburg", "state":"Virginia"},
		{"name":"University of Virginia", "city":"Charlottesville", "state":"Virginia"}
		]
	model = School
	url = '/api/v1/schools/'

	def test_create_school(self):
		school = self.school_list[0]
		response = json_response_to_dict(
			post_request(
				self.client,
				self.url,
				school
				)
			)
		self.assertEqual(
			response["status"],
			True
			)
		self.assertEqual(
			len(self.model.objects.all()),
			1
			)
		self.assertEqual(
			response['response']['name'],
			school['name']
			)

	def test_create_school_with_nonunique_name(self):
		school = self.school_list[0]
		status = post_request(
			self.client,
			self.url,
			[school, school]
			)
		self.assertEqual(
			status,
			False,
			"Incorrect response"
			)
		self.assertEqual(
			len(School.objects.all()),
			1,
			"Incorrect number of school objects"
			)

	def test_get_school_by_id(self):
		school = self.school_list[0]
		post_request(
			self.client,
			self.url,
			school
			)
		response = json_response_to_dict(
			get_request(
				self.client,
				self.url,
				pk=1
				)
			)
		self.assertEqual(
			response['response']['name'],
			school['name'],
			"Incorrect school name"
			)

	def test_get_all_schools(self):
		post_request(
			self.client,
			self.url,
			self.school_list
			)
		response = json_response_to_dict(
			get_request(
				self.client,
				self.url
				)
			)
		self.assertEqual(
			len(response['response']),
			len(self.school_list),
			"Incorrect number of schools"
			)

