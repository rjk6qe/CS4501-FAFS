from django.test import TestCase
from django.contrib.auth import authenticate
from fafs_api.models import User, School, UserManager, Category, Product
from fafs_api.admin import authenticate

import json

# Create your tests here.

def json_response_to_dict(response):
	return json.loads(response.content.decode('utf-8'))

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
		r = client.post(
			url,
			data=json.dumps(data),
			content_type="application/json"
			)
		return r
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
		s = School.objects.get_or_create(
			name=data['name'],
			city=data['city'],
			state=data['state']
			)
		return s
	if model == User:
		u = User.objects.get_or_create(
			email=data['email'],
			password=data['password'],
			school_id=School.objects.get()
		)
		return u
	if model == Category:
		c = Category.objects.get_or_create(
			name=data['name'],
			description=data['description']
		)
		return c

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
		create_model(School, self.school_values)

	def test_create_user(self):
		user = self.user_list[0]
		user['school_id'] = School.objects.get().pk
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
		user['school_id'] = School.objects.get().pk
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
		user['school_id'] = School.objects.get().pk
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
		user['school_id'] = School.objects.get().pk
		response = json_response_to_dict(
			post_request(
				self.client,
				self.url,
				data=user,
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
		for i in self.user_list:
			i['school_id'] = School.objects.get().pk
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
		user['school_id'] = School.objects.get().pk
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
		for i in self.user_list:
			i['school_id'] = School.objects.get().pk
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
		user['school_id'] = School.objects.get().pk
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
		user['school_id'] = School.objects.get().pk
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
		response = json_response_to_dict(
			post_request(
				self.client,
				self.url,
				school
				)
			)
		self.assertEqual(
			response['status'],
			True,
			"incorrect response"
			)
		school_pk = School.objects.get(name=response['response']['name']).pk
		response = json_response_to_dict(
			get_request(
				self.client,
				self.url,
				pk=school_pk
				)
			)
		self.assertEqual(
			response['status'],
			True,
			"Incorrect response"
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

class test_category(TestCase):

	category_list = [
		{"name":"Furniture", "description":"Stuff you put in your house"},
		{"name":"Clothing", "description":"Stuff you wear"}
		]
	model = Category
	url = '/api/v1/categories/'

	def test_create_category(self):
		category = self.category_list[0]
		response = json_response_to_dict(
			post_request(
				self.client,
				self.url,
				category
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
			category['name']
			)
		self.assertEqual(
			response['response']['description'],
			category['description']
		)

	def test_get_category_by_id(self):
		category = self.category_list[0]
		response = json_response_to_dict(
			post_request(
				self.client,
				self.url,
				category
				)
			)
		self.assertEqual(
			response['status'],
			True,
			"incorrect response"
			)
		category_pk = Category.objects.get(name=response['response']['name']).pk
		response = json_response_to_dict(
			get_request(
				self.client,
				self.url,
				pk=category_pk
				)
			)
		self.assertEqual(
			response['status'],
			True,
			"Incorrect response"
			)
		self.assertEqual(
			response['response']['name'],
			category['name'],
			"Incorrect category name"
			)
		self.assertEqual(
			response['response']['description'],
			category['description'],
			"Incorrect category description"
			)

	def test_get_all_categories(self):
		post_request(
			self.client,
			self.url,
			self.category_list
			)
		response = json_response_to_dict(
			get_request(
				self.client,
				self.url
				)
			)
		self.assertEqual(
			len(response['response']),
			len(self.category_list),
			"Incorrect number of categories"
			)

class test_product(TestCase):
	school_values = {"name":"University of Virginia", "city":"Charlottesville", "state":"Virginia"}
	user_list = [
		{"email":"gmail@gmail.com", "password":"password1","school_id":"1"}
	]
	category_list = [
		{"name":"Furniture", "description":"Stuff you put in your house"},
		{"name":"Clothing", "description":"Stuff you wear"}
	]
	product_list = [
	{
		"name":"Queen Mattress",
		"description":"Queen size mattress, never used.",
		"category_id":"1",
		"price":"300",
		"owner_id":"1",
		"time_posted":"2016-09-01T13:10:30",
		"time_updated":"2016-09-19T13:20:30",
		"pick_up":"pick up in the alley behind pigeonhole",
		"status":"N"
	},
	{
		"name":"White pants",
		"description":"Men's pants. White. 33x30.",
		"category_id":"1",
		"price":"15",
		"owner_id":"1",
		"time_posted":"2016-10-02T13:00:30",
		"time_updated":"2016-10-10T13:20:30",
		"pick_up":"pick up at crossroads",
		"status":"UP"
	}
	]
	model = Product
	url = '/api/v1/products/'

	def setUp(self):
		create_model(School, self.school_values)
		create_model(User, self.user_list[0])
		create_model(Category, self.category_list[0])


	def test_create_product(self):
		product = self.product_list[0]
		product['owner_id'] = User.objects.get().pk
		product['category_id'] = Category.objects.get().pk

		response = json_response_to_dict(
			post_request(
				self.client,
				self.url,
				product
				)
			)
		self.assertEqual(
			response["status"],
			True,
			response['response']
			)
		self.assertEqual(
			len(self.model.objects.all()),
			1
			)
		self.assertEqual(
			response['response']['name'],
			product['name'],
			"Wrong product name"
			)
		self.assertEqual(
			response['response']['description'],
			product['description'],
			"Wrong product description"
		)
		self.assertEqual(
			response['response']['pick_up'],
			product['pick_up'],
			"Wrong product pick up location"
		)

	def test_get_product_by_id(self):
		product = self.product_list[0]
		product['owner_id'] = User.objects.get().pk
		product['category_id'] = Category.objects.get().pk

		response = json_response_to_dict(
			post_request(
				self.client,
				self.url,
				product
				)
			)
		self.assertEqual(
			response['status'],
			True,
			response['response']
			#"incorrect response"
			)
		product_pk = Product.objects.get(name=response['response']['name']).pk
		response = json_response_to_dict(
			get_request(
				self.client,
				self.url,
				pk=product_pk
				)
			)
		self.assertEqual(
			response['status'],
			True,
			"Incorrect response"
			)
		self.assertEqual(
			response['response']['name'],
			product['name'],
			"Wrong product name"
			)
		self.assertEqual(
			response['response']['description'],
			product['description'],
			"Wrong product description"
		)
		self.assertEqual(
			'time_posted' in response['response'].keys(),
			True,
			"time not posted"
		)
		self.assertEqual(
			response['response']['pick_up'],
			product['pick_up'],
			"Wrong product pick up location"
		)
	"""
	def test_get_all_products(self):
		post_request(
			self.client,
			self.url,
			self.product_list
			)
		response = json_response_to_dict(
			get_request(
				self.client,
				self.url
				)
			)
		self.assertEqual(
			len(response['response']),
			len(self.product_list),
			"Incorrect number of products"
			)
	"""
