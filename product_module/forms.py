from django import forms
from .models import DiscountCode



class DiscountCodeForm(forms.Form):
    code = forms.CharField(label='کد تخفیف')

    def clean_code(self):
        code = self.cleaned_data.get('code')
        try:
            discount_code = DiscountCode.objects.get(code=code)
            if not discount_code.is_active():
                raise forms.ValidationError("کد تخفیف منقضی شده است.")
        except DiscountCode.DoesNotExist:
            raise forms.ValidationError("کد تخفیف وارد شده معتبر نیست.")
        return code
    
