from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.core.exceptions import ValidationError

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json

from fafs_api.models import User, School

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