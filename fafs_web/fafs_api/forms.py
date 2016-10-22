from django import forms

class UserRegister(forms.Form):
    email = forms.CharField(label='Enter email:', required=False, max_length=100)
    school = forms.CharField(label='Enter school:', required=False, max_length=100)
    phone_number = forms.CharField(label='Enter phone number:', required=False, max_length=100)
    password = forms.CharField(label='Enter password:', required=False, max_length=100)
