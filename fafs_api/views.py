from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.core.exceptions import ValidationError

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json

from fafs_api.models import User, Address, School, Category, Product, Transaction

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

class UserView(View):
	required_fields = ['email', 'school_id', 'password']
	model = User

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(UserView, self).dispatch(request, *args, **kwargs)

	def get(self, request, pk=None):
		if pk is not None:
			queryset = get_object_or_404(
				self.model,
				pk=pk
				)
			json_data = json.dumps({
				"pk":queryset.pk,
				"email":queryset.email,
				"school_id":queryset.school_id.pk,
				"rating":queryset.rating
				})
		else:
			queryset = self.model.objects.all()
			json_data = json.dumps(list(queryset.values('pk','email','school_id','rating')))
		return HttpResponse(json_data)

	def post(self, request):
		status = 200
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
			json_data = json.dumps({
				"pk":user.pk,
				"email":user.email,
				"rating":user.rating,
				"school_id":user.school_id.pk
				})
		except ValidationError as e:
			json_data = json.dumps(e.message_dict)
			status = 400
		return HttpResponse(json_data,status=status)

class AddressView(View):
	required_fields = ['street_number', 'street_name', 'city', 'state', 'zipcode', 'description']
	model = Address

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(AddressView, self).dispatch(request, *args, **kwargs)

	def get(self, request, pk=None):
		if pk is not None:
			queryset = get_object_or_404(
				self.model,
				pk=pk
			)
			json_data = json.dumps({
				"pk": queryset.pk,
				"street_number": queryset.street_number,
				"street_name": queryset.street_name,
				"city": queryset.city,
				"state": queryset.state,
				"zipcode": queryset.zipcode,
				"description": queryset.description,
				"address_2": queryset.address_2
			})
		else:
			queryset = self.model.objects.all()
			json_data = json.dumps(list(queryset.values('pk', 'street_number', 'street_name',
				'city', 'state', 'zipcode', 'address_2')))
		return HttpResponse(json_data)

	def post(self, request):
		status = 200
		json_data = json.loads(request.body.decode('utf-u'))
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
			json_data = json.dumps({
				"street_number": address.street_number,
				"street_name": address.street_name,
				"city": address.city,
				"state": address.state,
				"zipcode": address.zipcode,
				"address_2": address.address_2
			})
		except ValidationError as e:
			status = 400
			json_data = json.dumps(e.message_dict)
		return HttpResponse(json_data, status=status)


class SchoolView(View):

	required_fields = ['name','city','state']
	model = School

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(SchoolView, self).dispatch(request, *args, **kwargs)

	def get(self, request, pk=None):
		if pk is not None:
			queryset = get_object_or_404(
				self.model,
				pk=pk)
			json_data = json.dumps({
				"pk":queryset.pk,
				"name":queryset.name,
				"city":queryset.city,
				"state":queryset.state
				})
		else:
			queryset = self.model.objects.all()
			json_data = json.dumps(list(queryset.values('pk','name','city','state')))
		return HttpResponse(json_data)

	def post(self, request):
		status = 200
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
			json_data = json.dumps({
				"name":school.name,
				"city":school.city,
				"state":school.state
				})
		except ValidationError as e:
			status = 400
			json_data = json.dumps(e.message_dict)
		return HttpResponse(json_data, status=status)

class CategoryView(View):
	required_fields = ['name', 'description']
	model = Category

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(CategoryView, self).dispatch(request, *args, **kwargs)

	def get(self, request, pk=None):
		if pk is not None:
			queryset = get_object_or_404(
				self.model,
				pk=pk
			)
			json_data = json.dumps({
				"pk": queryset.pk,
				"name": queryset.name,
				"description": queryset.description
			})
		else:
			queryset = self.model.objects.all()
			json_data = json.dumps(list(queryset.values('pk', 'name', 'description')))
		return HttpResponse(json_data)

	def post(self, request):
		status = 200
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
			json_data = json.dumps({
				"name": category.name,
				"description": category.description
			})
		except ValidationError as e:
			status = 400
			json_data = json.dumps(e.message_dict)
		return HttpResponse(json_data, status=status)

class ProductView(View):
	required_fields = ['name', 'description', 'category_id', 'price', 'owner_id', 'pick_up']
	model = Product

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(ProductView, self).dispatch(request, *args, **kwargs)

	def get(self, request, pk=None):
		if pk is not None:
			queryset = get_object_or_404(
				self.model,
				pk=pk
			)
			json_data = json.dumps({
				"pk": queryset.pk,
				"name": queryset.name,
				"description": queryset.description,
				"category_id": queryset.category_id.pk,
				"price": queryset.price,
				"owner_id": queryset.owner_id.pk,
				"pick_up": queryset.pick_up,
				"time_posted": queryset.time_posted,
				"time_updated": queryset.time_updated
			})
		else:
			queryset = self.model.objects.all()
			json_data = json.dumps(list(queryset.values('pk','name','description',
				'category_id', 'price', 'owner_id', 'pick_up', 'time_posted', 'time_updated')))
		return HttpResponse(json_data)

	def post(self, request):
		status = 200
		json_data = json.loads(request.body.decode('utf-8'))
		field_dict = retrieve_all_fields(
			json_data,
			self.required_fields
		)

		try:
			product = self.model(
				name=field_dict['name'],
				description=field_dict['description'],
				category_id=field_dict['category_id'],
				price=field_dict['price'],
				owner_id=ield_dict['owner_id'],
				pick_up=field_dict['pick_up']
			)
			product.clean()
			product.save()
			json_data = json.dumps({
				"name": product.name,
				"description": product.description,
				"category_id": product.category_id.pk,
				"price": product.price,
				"owner_id": product.owner_id.pk,
				"pick_up": product.pick_up,
			})
		except ValidationError as e:
			status = 400
			json_data = json.dumps(e.message_dict)
		return HttpResponse(json_data, status=status)


class TransactionView(View):
	required_fields = ['seller', 'buyer', 'product_id']
	model = Transaction

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(TransactionView, self).dispatch(request, *args, **kwargs)

	def get(self, request, pk=None):
		if pk is not None:
			queryset = get_object_or_404(
				self.model,
				pk=pk
			)
			json_data = json.dumps({
				"pk": queryset.pk,
				"seller": queryset.seller,
				"buyer": queryset.buyer,
				"product_id": queryset.product_id
			})
		else:
			queryset = self.model.objects.all()
			json_data = json.dumps(list(queryset.values('pk', 'seller', 'buyer', 'product_id')))
		return HttpResponse(json_data)

	def post(self, request):
		status = 200
		json_data = json.loads(request.body.decode('utf-8'))
		field_dict = retrieve_all_fields(
			json_data,
			self.required_fields
		)
		try:
			transaction = self.model(
				seller=field_dict['seller'],
				buyer=field_dict['buyer'],
				product_id=field_dict['product_id']
			)
			transaction.clean()
			transaction.save()
			json_data = json.dumps({
				"seller": transaction.seller,
				"buyer": transaction.buyer,
				"product_id": transaction.product_id
			})
		except ValidationError as e:
			status = 400
			json_data = json.dumps(e.message_dict)
		return HttpResponse(json_data, status=status)