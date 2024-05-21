from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from iranian_cities.models import Ostan, Shahrestan
from account_module.models import User


                

# TODO : CHANGE THIS like your new model
class EditProfileModelForm(forms.ModelForm):

    ostan = forms.ModelChoiceField(
        queryset=Ostan.objects.all(),
        label='استان'
    )
    shahrestan = forms.ModelChoiceField(
        queryset=Shahrestan.objects.none(),
        label='شهر'
    )


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'ostan', 'shahrestan','street','postal_code']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control','required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','required': True}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control','requried': True,'maxlength': '11', 'minlength': '11'}),
            'ostan': forms.Select(attrs={'class': 'form-control','rows': 1,'required': True}),
            'shahrestan': forms.Select(attrs={'class': 'form-control','rows': 1,'required': True}),
            'street': forms.Textarea(attrs={'class': 'form-control','rows': 1,'required': True}),
            'postal_code': forms.NumberInput(attrs={'class': 'form-control','rows': 1,'id': 'message','required': True,'maxlength': '10', 'minlength': '10'})
            }
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'phone_number': 'شماره تلفن',
            'street': 'خیابان',
            'postal_code': 'کد پستی',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'ostan' in self.data:
            try:
                ostan_id = int(self.data.get('ostan'))
                self.fields['shahrestan'].queryset = Shahrestan.objects.filter(ostan_id=ostan_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['shahrestan'].queryset = Shahrestan.objects.none()
        elif self.instance and self.instance.pk:
            self.fields['shahrestan'].queryset = Shahrestan.objects.filter(ostan_id=self.instance.ostan_id).order_by('name')
            if self.instance.shahrestan:
                self.fields['shahrestan'].initial = self.instance.shahrestan




    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 11:
            raise ValidationError("شماره تلفن باید دقیقا 11 رقم باشد.")
        return phone_number

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if len(postal_code) != 10:
            raise ValidationError("کد پستی باید دقیقا 10 رقم باشد.")
        return postal_code
    


    
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
