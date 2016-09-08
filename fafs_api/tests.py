from django.test import TestCase
from django.contrib.auth import authenticate
from fafs_api.models import User, School, UserManager

# Create your tests here.

class test_api(TestCase):

	set_password = 'helloworld'
	set_email = 'rjk6qe@virginia.edu'

	def setUp(self):
		s = School.objects.create(name='UVA', city='Charlottesville', state='Virginia')
		User.objects.create_user(email=self.set_email, school = s, password=self.set_password)

	def test_create_school(self):
		self.assertEqual(len(School.objects.all()),1, "School was not created")

	def test_create_user(self):
		self.assertNotEqual(User.objects.get().password, self.set_password, "Password was not hashed")

	def test_authenticate_user(self):
		user = authenticate(username=self.set_email, password= self.set_password)
		self.assertNotEqual(user, None, "User could not be authenticated")