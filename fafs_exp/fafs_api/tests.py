from django.test import TestCase
from django.core.exceptions import ValidationError

import json


def json_response_to_dict(response):
	try:
		return json.loads(response.content.decode('utf-8'))
	except json.decoder.JSONDecodeError:
		raise ValidationError(response.content.decode('utf-8'))


class UserStoryOne(TestCase):
#Buyer/Seller logs in, see personalized content

	base_url = '/fafs/'

	def append_url(self, path_list):
		url = self.base_url
		for path in path_list:
			url = url + str(path) + '/'
		return url

	def post_request(self, path_list, data):
		#Takes in path list, dictionary
		url = self.append_url(path_list)
		response = json_response_to_dict(
			self.client.post(
				url,
				data = json.dumps(data),
				content_type="application/json"
				)
			)
		return response

	def get_request(self, path_list):
		url = self.append_url(path_list)
		response = json_response_to_dict(
			self.client.get(
				url
				)
			)
		return response

	buyer_data = {'email':'a@a.com','password':'a','school_id':1}
	seller_data = {'email':'b@b.com', 'password':'b', 'school_id':1}

	register_url_list = ['register', ]
	login_url_list = ['login', ]


	def setUp(self):
		response = self.get_request(
			['school',]
			)
		if response['status']:
			self.buyer_data['school_id'] = response['response']['pk']
			self.seller_data['school_id'] = response['response']['pk']
		self.post_request(
			self.register_url_list,
			self.buyer_data
			)

	def test_user_login_success(self):
		response = self.post_request(
			self.login_url_list,
			self.buyer_data
			)
		self.assertEqual(
			response['status'],
			True,
			"Incorrect status on login"
			)

	def test_seller_create_listing(self):
		response = self.post_request(
			self.login_url_list,
			self.buyer_data
			)
		data = {'name':'test','description':'test_descr','pick_up':'sfdds','price':'500','owner_id':1, 'category_id':1}
		response = self.post_request(
			['products','create'],
			data
			)
		self.assertEqual(
			response['status'],
			True,
			"Incorrect status on product creation"
			)

	def test_register_user(self):
		response = self.post_request(
			self.register_url_list,
			self.seller_data
			)
		self.assertEqual(
			response['status'],
			True,
			"Valid user could not be created" + str(response)
			)
		response = self.post_request(
			self.register_url_list,
			self.seller_data
			)
		self.assertEqual(
			response['status'],
			False,
			"Invalid user was created when it shouldn't have been"
			)

	def test_create_product(self):
		data = {'name':'test','description':'test_descr','pick_up':'sfdds','price':'500','owner_id':1, 'category_id':1}

		self.post_request(
			self.login_url_list,
			self.seller_data
			)

		response = self.post_request(
			['products','create'],
			data
			)

		self.assertEqual(
			response['status'],
			True,
			"Unable to create a product while logged in"
			)

	def test_search_no_keyword(self):
		data = {"keyword": ""}

		response = self.post_request(
			['search_products'],
			data
			)

		self.assertEqual(
			len(response['hits']),
			0,
			"Response with no search returns a hit"
			)

	def test_search_created_product_by_name(self):
		data = {'name':'banana','description':'apples','pick_up':'rice','price':'500','owner_id':1, 'category_id':1}
		self.post_request(
		 		self.login_url_list,
		 		self.seller_data
		 	)

		response = self.post_request(
			['products', 'create'],
			data
		)

		data = {"keyword": "banana"}
		search_response = self.post_request(
			['search_products'],
			data
		)

		self.assertEqual(
			len(search_response['hits']) > 0,
			True,
			"Response with created product returns nothing"
		)

	def test_search_created_product_by_description(self):
		data = {'name':'banana','description':'apples','pick_up':'rice','price':'500','owner_id':1, 'category_id':1}
		self.post_request(
		 		self.login_url_list,
		 		self.seller_data
		 	)

		response = self.post_request(
			['products', 'create'],
			data
		)

		data = {"keyword": "apples"}
		search_response = self.post_request(
			['search_products'],
			data
		)

		self.assertEqual(
			len(search_response['hits']) > 0,
			True,
			"Response with created product returns nothing"
		)

	def test_search_wrong_keyword(self):
		data = {"keyword": "asdfasdfasdfadf"}

		search_response = self.post_request(
			['search_products'],
			data
		)

		self.assertEqual(
			len(search_response['hits']),
			0,
			"Response with random keyword returns hit"
		)

	def test_search_created_product_by_pick_up(self):
		data = {'name':'banana','description':'apples','pick_up':'rice','price':'500','owner_id':1, 'category_id':1}
		self.post_request(
		 		self.login_url_list,
		 		self.seller_data
		 	)

		response = self.post_request(
			['products', 'create'],
			data
		)

		data = {"keyword": "rice"}
		search_response = self.post_request(
			['search_products'],
			data
		)

		self.assertEqual(
			len(search_response['hits']) > 0,
			True,
			"Response with created product and close keyword returns nothing"
		)
