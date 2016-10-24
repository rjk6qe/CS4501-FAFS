from django import forms
from . import views

class UserRegister(forms.Form):
    email = forms.CharField(label='Enter email:', required=True, max_length=100)
    school = forms.CharField(label='Enter school:', required=True, max_length=100)
    password = forms.CharField(label="Enter password:",
                                required=True,
                                max_length=100,
                                widget=forms.PasswordInput)

class UserLoginForm(forms.Form):
    email = forms.CharField(label='Enter email:', required=True, max_length=100)
    password = forms.CharField(label="Enter password:",
                                required=True,
                                max_length=100,
                                widget=forms.PasswordInput)
    next = forms.CharField(required=False,
                            max_length=100,
                            widget=forms.HiddenInput)

class ProductForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=500,
                                    widget=forms.Textarea)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    pick_up = forms.CharField(max_length=50)

    OFF_MARKET = 'OM'
    FOR_SALE = 'FS'
    NEGOTIATING = 'N'
    SOLD = 'S'
    EXCHANGED = 'E'

    STATUS_CHOICES = (
        (OFF_MARKET, 'Off the market'),
        (FOR_SALE, 'For Sale'),
        (NEGOTIATING, 'Negotiating'),
        (SOLD, 'Sold'),
        (EXCHANGED, 'Exchanged'),
    )
    status = forms.ChoiceField(
                                choices=STATUS_CHOICES,
                                initial=FOR_SALE)

    NEW = 'N'
    USED_GOOD = 'UG'
    USED_OKAY = 'UO'
    USED_POOR = 'UP'

    CONDITION_CHOICES = (
        (NEW, 'New condition'),
        (USED_GOOD, 'Used and in good condition'),
        (USED_OKAY, 'Used and in okay condition'),
        (USED_POOR, 'Used and in poor condition')
    )
    condition = forms.ChoiceField(choices=CONDITION_CHOICES,
                                    initial=NEW)

    def __init__(self, *args, **kwargs):
        category_choices = kwargs.pop('category_choices', None)

        super(ProductForm, self).__init__(*args, **kwargs)
        if category_choices:
            self.fields['category_id'] = forms.ChoiceField(
                                choices=category_choices,
                                label='Category')
        self.field_order = ['name', 'description', 'category_id']
