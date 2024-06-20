from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView
from account_module.models import User
from order_module.models import Order, OrderDetail
from .forms import EditProfileModelForm, ChangePasswordForm
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from iranian_cities.models import Shahrestan
from product_module.models import DiscountCode
from product_module.forms import DiscountCodeForm
from django.contrib import messages
from django.db.models import Q


@method_decorator(login_required, name='dispatch')
class UserPanelDashboardPage(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard_page.html'


@method_decorator(login_required, name='dispatch')
class EditUserProfilePage(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(instance=current_user)
        context = {
            'form': edit_form,
            'current_user': current_user
        }
    
        return render(request, 'user_panel_module/edit_profile_page.html', context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)

        context = {
            'form': edit_form,
            'current_user': current_user
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context)


@method_decorator(login_required, name='dispatch')
class ChangePasswordPage(View):
    def get(self, request: HttpRequest):
        context = {
            'form': ChangePasswordForm()
        }
        return render(request, 'user_panel_module/change_password_page.html', context)

    def post(self, request: HttpRequest):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_user: User = User.objects.filter(id=request.user.id).first()
            if current_user.check_password(form.cleaned_data.get('current_password')):
                current_user.set_password(form.cleaned_data.get('password'))
                current_user.save()
                logout(request)
                return redirect(reverse('login_page'))
            else:
                form.add_error('password', 'کلمه عبور وارد شده اشتباه می باشد')

        context = {
            'form': form
        }
        return render(request, 'user_panel_module/change_password_page.html', context)


@method_decorator(login_required, name='dispatch')
class MyShopping(ListView):
    model = Order
    template_name = 'user_panel_module/user_shopping.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = self.request.GET.get('activeTab', 'in_progress')
        return context

    def get_queryset(self):
        active_tab = self.request.GET.get('activeTab')
        if   active_tab == 'in_progress':
            queryset = Order.objects.filter(user=self.request.user, is_paid=True).filter(Q(status='shipped') | Q(status='processing')).order_by('-id')
        elif active_tab ==        'sent':
            queryset = Order.objects.filter(user=self.request.user, is_paid=True, status='delivered')
        elif active_tab ==    'returned':
            queryset = Order.objects.filter(user=self.request.user, is_paid=True, status='returned')
        elif active_tab ==   'cancelled':
            queryset = Order.objects.filter(user=self.request.user, is_paid=True, status='cancelled')
        else:
            queryset = Order.objects.filter(user=self.request.user, is_paid=True).filter(Q(status='shipped') | Q(status='processing'))
        return queryset


@login_required
def user_panel_menu_component(request: HttpRequest):
    return render(request, 'user_panel_module/components/user_panel_menu_component.html')



from django.contrib import messages

@login_required
def user_basket(request: HttpRequest):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    # اگر کاربر فرم کد تخفیف را ارسال کرده باشد
    if request.method == 'POST':
        discount_form = DiscountCodeForm(request.POST)
        if discount_form.is_valid():
            code = discount_form.cleaned_data['code']
            try:
                discount_code = DiscountCode.objects.get(code=code)
                if discount_code.is_active():
                    # اعمال تخفیف به قیمت کل سبد خرید
                    discount_amount = (total_amount * discount_code.discount_percentage) / 100
                    total_amount -= discount_amount

                    # ذخیره کد تخفیف در مدل Order
                    current_order.discount_code = discount_code
                    current_order.save()

                    # ذخیره مبلغ تخفیف در مدل Order یا هر جای مناسب دیگر
                    current_order.discount_amount = discount_amount
                    current_order.save()

                    # بازگرداندن به همین صفحه یا مرحله بعدی
                    messages.success(request, "کد تخفیف با موفقیت اعمال شد.")
                    return redirect('user_basket_page')
                else:
                    messages.error(request, "کد تخفیف منقضی شده است.")
            except DiscountCode.DoesNotExist:
                messages.error(request, "کد تخفیف وارد شده معتبر نیست.")
    
    else:
        discount_form = DiscountCodeForm()

    profile_form = EditProfileModelForm(instance=request.user)

    context = {
        'order': current_order,
        'sum': total_amount,
        'profile_form': profile_form,
        'discount_form': discount_form,  # اضافه کردن فرم کد تخفیف به context
    }
    return render(request, 'user_panel_module/user_basket.html', context)


@login_required
def remove_discount_code(request):
    if request.method == 'POST':
        current_order = Order.objects.filter(user=request.user, is_paid=False).first()
        if current_order:
            current_order.discount_code = None
            current_order.discount_amount = 0
            current_order.save()
            messages.success(request, "کد تخفیف با موفقیت از سبد خرید حذف شد.")
        else:
            messages.error(request, "سبد خرید شما خالی است یا کد تخفیفی برای حذف وجود ندارد.")
    return redirect('user_basket_page')


def user_basket2(request):
    # اینجا می‌توانید لازمه برای ایجاد فرم اطلاعات فردی کاربر را انجام دهید
    # برای مثال:
    if request.method == 'POST':
        profile_form = EditProfileModelForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('request_payment')  # فرم معتبر بود، به مرحله بعدی هدایت می‌شود
    else:
        profile_form = EditProfileModelForm(instance=request.user)
        
    context = {
        'profile_form': profile_form,
    }
    return render(request, 'user_panel_module/user_basket2.html', context)

def load_shahrestans(request):
    ostan_id = request.GET.get('ostan')
    shahrestans = Shahrestan.objects.filter(ostan_id=ostan_id).order_by('name')
    return JsonResponse(list(shahrestans.values('id', 'name')), safe=False)


@login_required
def remove_order_detail(request):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })

    deleted_count, deleted_dict = OrderDetail.objects.filter(id=detail_id, order__is_paid=False, order__user_id=request.user.id).delete()

    if deleted_count == 0:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/user_basket_content.html', context)
    })


@login_required
def change_order_detail_count(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found_detail_or_state'
        })

    order_detail = OrderDetail.objects.filter(id=detail_id, order__user_id=request.user.id, order__is_paid=False).first()

    if order_detail is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    if state == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_invalid'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/user_basket_content.html', context)
    })


def my_shopping_detail(request: HttpRequest, order_id):
    order = Order.objects.prefetch_related('orderdetail_set').filter(id=order_id, user_id=request.user.id).first()
    if order is None:
        raise Http404('سبد خرید مورد نظر یافت نشد')

    return render(request, 'user_panel_module/user_shopping_detail.html', {
        'order': order
    })


# ///////////////////////////////////////////////
from django.shortcuts import render, get_object_or_404


def print_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'user_panel_module/print_invoice.html', {
        'order': order
    })