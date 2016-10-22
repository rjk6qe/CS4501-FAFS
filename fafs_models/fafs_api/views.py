from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.core.exceptions import ValidationError
from django.contrib.auth import hashers
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json

from fafs_api.models import User, Address, School, Category, Product, Transaction, Authenticator

def get_key(dictionary, key):
	try:
		return dictionary[key]
	except KeyError:
		return None

def retrieve_all_fields(dictionary, field_list):
	return_dict = {}
	for field in field_list:
		value = get_key(dictionary, field)
		return_dict[field] = value
	return return_dict

def get_object_or_none(model, pk):
	try:
		return model.objects.get(pk=pk)
	except model.DoesNotExist:
		return None

def json_encode_dict_and_status(dictionary, status):
	response_dict = {}
	response_dict["status"] = status
	response_dict["response"] = dictionary
	return response_dict

class LoginView(View):
	model = User
	required_fields = ['email', 'password']

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(LoginView, self).dispatch(request, *args, **kwargs)

	def post(self, request):
		print("login request!")
		status = False
		print(json.loads(request.body.decode('utf-8')))
		json_data = json.loads(request.body.decode('utf-8'))
		print("Json data:", json_data)
		field_dict = retrieve_all_fields(
						json_data,
						self.required_fields
					)
		json_data = {"message": "Invalid login"}
		try:
			login_user = User.objects.get(email=field_dict['email'])
			hashed_password = login_user.password
			if hashers.check_password(field_dict['password'], hashed_password):
				authenticator = Authenticator()
				authenticator.user = login_user
				authenticator.save()
				json_data = {
					"token": authenticator.token,
					"email": authenticator.user.email,
					"date_created": authenticator.date_created
				}
				status = True
		except User.DoesNotExist:
			pass
		return JsonResponse(json_encode_dict_and_status(json_data, status))

class LogoutView(View):
	required_fields = ['authenticator']

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(LogoutView, self).dispatch(request, *args, **kwargs)

	def post(self, request):
		status = False
		json_data = json.loads(request.body.decode('utf-8'))
		field_dict = retrieve_all_fields(
						json_data,
						self.required_fields
					)
		try:
			auth = Authenticator.objects.get(token=field_dict['authenticator'])
			auth.delete()
			status = True
			json_data = {}
		except Authenticator.DoesNotExist:
			status = False
			json_data = {'message': 'Invalid authenticator'}
		return JsonResponse(json_encode_dict_and_status(json_data, status))


class UserView(View):
	required_fields = ['email', 'school_id', 'password']
	update_fields = ['user_pk','email','password']
	model = User

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(UserView, self).dispatch(request, *args, **kwargs)

	def get(self, request, pk=None):
		status = False
		if pk is not None:
			queryset = get_object_or_none(
				self.model,
				pk=pk
				)
			if queryset is not None:
				status = True
				json_data = {
					"pk":queryset.pk,
					"email":queryset.email,
					"school_id":queryset.school_id.pk,
					"rating":queryset.rating
					}
			else:
				status = False
				json_data = {}
		else:
			status = True
			queryset = self.model.objects.all()
			json_data = list(queryset.values('pk','email','school_id','rating'))

		return JsonResponse(json_encode_dict_and_status(json_data, status))

	def post(self, request):
		status = True
		json_data = json.loads(request.body.decode('utf-8'))
		field_dict = retrieve_all_fields(
			json_data,
			self.required_fields
			)
		try:
			user = self.model.objects.create_user(
				email=field_dict['email'],
				password=field_dict['password'],
				school=field_dict['school_id']
				)
			json_data = {
				"pk":user.pk,
				"email":user.email,
				"rating":user.rating,
				"school_id":user.school_id.pk
				}
		except ValidationError as e:
			json_data = e.message_dict
			status = False
		return JsonResponse(json_encode_dict_and_status(json_data, status))

	def patch(self, request):
		status = True
		json_data = json.loads(request.body.decode('utf-8'))
		field_dict = retrieve_all_fields(
			json_data,
			self.update_fields
			)
		try:
			user = self.model.objects.update_user(
				user_pk = get_key(field_dict,'user_pk'),
				email = get_key(field_dict,'email'),
				password = get_key(field_dict,'password')
				)
			json_data = {
				"pk":user.pk,
				"email":user.email,
				"rating":user.rating,
				"school_id":user.school_id.pk
				}
		except ValidationError as e:
			json_data = e.message_dict
			status = False
		return JsonResponse(json_encode_dict_and_status(json_data, status))

	def delete(self, request, pk=None):
		status = False
		obj = get_object_or_none(self.model, pk)
		if obj is not None:
			obj.delete()
			status = True
		return JsonResponse(json_encode_dict_and_status({},status))


class AddressView(View):
	required_fields = ['street_number', 'street_name', 'city', 'state', 'zipcode', 'description']
	model = Address

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(AddressView, self).dispatch(request, *args, **kwargs)

	def get(self, request, pk=None):
		status = True
		if pk is not None:
			queryset = get_object_or_none(
				self.model,
				pk=pk
			)
			if queryset is not None:
				json_data = {
					"pk": queryset.pk,
					"street_number": queryset.street_number,
					"street_name": queryset.street_name,
					"city": queryset.city,
					"state": queryset.state,
					"zipcode": queryset.zipcode,
					"description": queryset.description,
					"address_2": queryset.address_2
				}
			else:
				status = False
				json_data = {}
		else:
			queryset = self.model.objects.all()
			json_data = list(queryset.values('pk', 'street_number', 'street_name',
				'city', 'state', 'zipcode', 'address_2'))
		return JsonResponse(json_encode_dict_and_status(json_data, status))

	def post(self, request):
		status = True
		json_data = json.loads(request.body.decode('utf-8'))
		field_dict = retrieve_all_fields(
			json_data,
			self.required_fields
		)
		try:
			address = self.model(
				street_number = field_dict['street_number'],
				street_name = field_dict['street_name'],
				city = field_dict['city'],
				state = field_dict['state'],
				zipcode = field_dict['zipcode'],
				address_2 = field_dict['address_2']
			)
			address.clean()
			address.save()
			json_data = {
				"street_number": address.street_number,
				"street_name": address.street_name,
				"city": address.city,
				"state": address.state,
				"zipcode": address.zipcode,
				"address_2": address.address_2
			}
		except ValidationError as e:
			status = False
			json_data = e.message_dict
		return JsonResponse(json_encode_dict_and_status(json_data, status))

	def delete(self, request, pk=None):
		status = False
		obj = get_object_or_none(self.model, pk)
		if obj is not None:
			obj.delete()
			status = True
		return JsonResponse(json_encode_dict_and_status({},status))


class SchoolView(View):

	required_fields = ['name','city','state']
	model = School

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(SchoolView, self).dispatch(request, *args, **kwargs)

	def get(self, request, pk=None):
		status = True
		if pk is not None:
			queryset = get_object_or_none(
				self.model,
				pk=pk)
			if queryset is not None:
				json_data = {
					"pk":queryset.pk,
					"name":queryset.name,
					"city":queryset.city,
					"state":queryset.state
					}
			else:
				status = False
				json_data = {}
		else:
			queryset = self.model.objects.all()
			json_data = list(queryset.values('pk','name','city','state'))
		return JsonResponse(json_encode_dict_and_status(json_data, status))

	def post(self, request):
		status = True
		json_data = json.loads(request.body.decode('utf-8'))
		field_dict = retrieve_all_fields(
			json_data,
			self.required_fields
			)
		try:
			school = self.model(
				name=field_dict['name'],
				city=field_dict['city'],
				state=field_dict['state']
				)
			school.clean()
			school.save()
			json_data = {
				"name":school.name,
				"city":school.city,
				"state":school.state
				}
		except ValidationError as e:
			status = False
			json_data = e.message_dict
		return JsonResponse(json_encode_dict_and_status(json_data, status))

	def delete(self, request, pk=None):
		status = False
		obj = get_object_or_none(self.model, pk)
		if obj is not None:
			obj.delete()
			status = True
		return JsonResponse(json_encode_dict_and_status({},status))


class CategoryView(View):
	required_fields = ['name', 'description']
	model = Category

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(CategoryView, self).dispatch(request, *args, **kwargs)

	def get(self, request, pk=None):
		status = True
		if pk is not None:
			queryset = get_object_or_none(
				self.model,
				pk=pk
			)
			if queryset is not None:
				json_data = {
					"pk": queryset.pk,
					"name": queryset.name,
					"description": queryset.description
				}
			else:
				status = False
				json_data = {}
		else:
			queryset = self.model.objects.all()
			json_data = list(queryset.values('pk', 'name', 'description'))
		return JsonResponse(json_encode_dict_and_status(json_data, status))

	def post(self, request):
		status = True
		json_data = json.loads(request.body.decode('utf-8'))
		field_dict = retrieve_all_fields(
			json_data,
			self.required_fields
		)
		try:
			category = self.model(
				name=field_dict['name'],
				description=field_dict['description']
			)
			category.clean()
			category.save()
			json_data = {
				"name": category.name,
				"description": category.description
			}
		except ValidationError as e:
			status = False
			json_data = e.message_dict
		return JsonResponse(json_encode_dict_and_status(json_data, status))

	def delete(self, request, pk=None):
		status = False
		obj = get_object_or_none(self.model, pk)
		if obj is not None:
			obj.delete()
			status = True
		return JsonResponse(json_encode_dict_and_status({},status))

	def delete(self, request, pk=None):
		status = False
		obj = get_object_or_none(self.model, pk)
		if obj is not None:
			obj.delete()
			status = True
		return JsonResponse(json_encode_dict_and_status({},status))


class ProductView(View):
	required_fields = ['name', 'description', 'category_id', 'price', 'owner_id', 'pick_up']
	model = Product

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(ProductView, self).dispatch(request, *args, **kwargs)

	def get(self, request, pk=None):
		status = True
		if pk is not None:
			queryset = get_object_or_none(
				self.model,
				pk=pk
			)
			if queryset is not None:
				json_data = {
					"pk": queryset.pk,
					"name": queryset.name,
					"description": queryset.description,
					"category_id": queryset.category_id.pk,
					"price": queryset.price,
					"owner_id": queryset.owner_id.pk,
					"pick_up": queryset.pick_up,
					"time_posted": queryset.time_posted,
					"time_updated": queryset.time_updated
				}
			else:
				status = False
				json_data = {}
		else:
			queryset = self.model.objects.all()
			json_data = list(queryset.values('pk','name','description',
				'category_id', 'price', 'owner_id', 'pick_up', 'time_posted', 'time_updated'))
		return JsonResponse(json_encode_dict_and_status(json_data, status))

	def post(self, request):
		status = True
		json_data = json.loads(request.body.decode('utf-8'))
		field_dict = retrieve_all_fields(
			json_data,
			self.required_fields
		)
		try:
			category = None
			owner = None
			try:
				category = Category.objects.get(pk=field_dict['category_id'])
				owner = User.objects.get(pk=field_dict['owner_id'])
			except (Category.DoesNotExist, User.DoesNotExist):
				raise ValidationError({
					"Error":"Invalid category or owner id"
					})
			product = self.model(
				name=field_dict['name'],
				description=field_dict['description'],
				category_id=category,
				price=field_dict['price'],
				owner_id=owner,
				pick_up=field_dict['pick_up']
			)
			product.clean()
			product.save()
			json_data = {
				"name": product.name,
				"description": product.description,
				"category_id": product.category_id.pk,
				"price": product.price,
				"owner_id": product.owner_id.pk,
				"pick_up": product.pick_up,
			}
		except ValidationError as e:
			status = False
			json_data = e.message_dict
		return JsonResponse(json_encode_dict_and_status(json_data, status))

	def delete(self, request, pk=None):
		status = False
		obj = get_object_or_none(self.model, pk)
		if obj is not None:
			obj.delete()
			status = True
		return JsonResponse(json_encode_dict_and_status({},status))



class TransactionView(View):
	required_fields = ['seller', 'buyer', 'product_id']
	model = Transaction

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(TransactionView, self).dispatch(request, *args, **kwargs)

	def get(self, request, pk=None):
		status = True
		if pk is not None:
			queryset = get_object_or_none(
				self.model,
				pk=pk
			)
			if queryset is not None:
				json_data = {
					"pk": queryset.pk,
					"seller": queryset.seller.pk,
					"buyer": queryset.buyer.pk,
					"product_id": queryset.product_id.pk
				}
			else:
				status = False
				json_data = {}
		else:
			queryset = self.model.objects.all()
			json_data = list(queryset.values('pk', 'seller', 'buyer', 'product_id'))
		return JsonResponse(json_encode_dict_and_status(json_data, status))

	def post(self, request):
		status = True
		json_data = json.loads(request.body.decode('utf-8'))
		field_dict = retrieve_all_fields(
			json_data,
			self.required_fields
		)
		try:
			seller_id = None
			buyer_id = None
			product_id = None
			try:
				seller_id = User.objects.get(pk=field_dict['seller'])
				buyer_id = User.objects.get(pk=field_dict['buyer'])
				product_id = Product.objects.get(pk=field_dict['product_id'])
			except User.DoesNotExist:
				raise ValidationError({
					"Error":"Invalid seller id"
					})
			transaction = self.model(
				seller=seller_id,
				buyer=buyer_id,
				product_id=product_id
			)
			transaction.clean()
			transaction.save()
			json_data = {
				"seller": transaction.seller.pk,
				"buyer": transaction.buyer.pk,
				"product_id": transaction.product_id.pk
			}
		except ValidationError as e:
			status = False
			json_data = e.message_dict
		return JsonResponse(json_encode_dict_and_status(json_data, status))

	def delete(self, request, pk=None):
		status = False
		obj = get_object_or_none(self.model, pk)
		if obj is not None:
			obj.delete()
			status = True
		return JsonResponse(json_encode_dict_and_status({},status))
