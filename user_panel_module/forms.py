from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from iranian_cities.models import Ostan

from account_module.models import User
from iranian_cities.models import Shahrestan

# TODO : CHANGE THIS like your new model
class EditProfileModelForm(forms.ModelForm):
    state = forms.ModelChoiceField(queryset=Ostan.objects.all(), label='استان', empty_label=None)
    city = forms.ModelChoiceField(queryset=Shahrestan.objects.none(), label='شهر', empty_label=None)  # افزودن فیلد شهر


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'state', 'city','street','postal_code']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control','required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','required': True}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control','requried': True}),
            'state': forms.Textarea(attrs={'class': 'form-control','rows': 1,'required': True}),
            'city': forms.Textarea(attrs={'class': 'form-control','rows': 1,'required': True}),
            'street': forms.Textarea(attrs={'class': 'form-control','rows': 1,'required': True}),
            'postal_code': forms.NumberInput(attrs={'class': 'form-control','rows': 1,'id': 'message','required': True})
            }
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'phone_number': 'شماره تلفن',
            'state': 'استان',
            'city': 'شهر',
            'street': 'کوچه',
            'postal_code': 'کد پستی',
        }



class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='کلمه عبور فعلی',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password

        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')
