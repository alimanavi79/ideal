import time
import logging
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.urls import reverse
from product_module.models import Product
from .models import Order, OrderDetail
from django.shortcuts import redirect, render
import requests
import json
from django.utils import timezone
from zeep import Client

# Create your views here.


MERCHANT = '44c9a34d-acec-46d6-8413-644e0480eb9d'

ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/services/WebGate/wsdl"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/services/WebGate/wsdl"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/{authority}"
# ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
# ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
# ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "نهایی کردن خرید شما از سایت ما"  # Required
email = ''  # Optional
mobile = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify-payment/'


def add_product_to_order(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))
    print('1')
    print(product_id)
    print('2')
    print(count)
    if count < 1:
        # count = 1
        return JsonResponse({
            'status': 'invalid_count',
            'text': 'مقدار وارد شده معتبر نمی باشد',
            'confirm_button_text': 'مرسی از شما',
            'icon': 'warning'
        })

    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()

        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)

            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()

            if current_order_detail is not None:

                current_order_detail.count += count
                current_order_detail.save()
            else:

                new_detail = OrderDetail(order=current_order, product=product, count=count)
                new_detail.final_price = new_detail.get_total_price()
                new_detail.save()

            return JsonResponse({
                'status': 'success',
                'text': 'محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد',
                'confirm_button_text': 'باشه ممنونم',
                'icon': 'success'
            })
        else:
            return JsonResponse({
                'status': 'not_found',
                'text': 'محصول مورد نظر یافت نشد',
                'confirm_button_text': 'مرسییییی',
                'icon': 'error'
            })
    else:
        return JsonResponse({
            'status': 'not_auth',
            'text': 'برای افزودن محصول به سبد خرید ابتدا می بایست وارد سایت شوید',
            'confirm_button_text': 'ورود به سایت',
            'icon': 'error'
        })
    

@login_required
def request_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    if total_price == 0:
        return redirect(reverse('user_basket_page'))
    print(total_price)
    req_data = {
        "merchant_id": MERCHANT,
        "amount": total_price * 10,
        "callback_url": CallbackURL,
        "description": description,
        # "metadata": {"mobile": mobile, "email": email}
        "metadata": {"mobile": "09123456789", "email": "a@b.com"}
    }

    client = Client(ZP_API_REQUEST)
    res = client.service.PaymentRequest(
        MERCHANT,
        total_price * 10,
        description,
        '',
        '',
        CallbackURL,
    )
    bodyResponse = res.Status
    authority = res.Authority
    if bodyResponse != 100:
        return HttpResponse('Error occurd')
        
    return redirect(ZP_API_STARTPAY.format(authority=authority))


@login_required
def verify_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": total_price * 10,
            "authority": t_authority
        }

        client = Client(ZP_API_VERIFY)
        res = client.service.PaymentVerification(
            MERCHANT,
            t_authority,
            total_price * 10,
        )
        bodyResponse = res.Status
        ref_str = res.RefID
        # if bodyResponse != 100:
        #     return HttpResponse('Error occurd')
        if bodyResponse ==100:
            current_order.is_paid = True
            current_order.payment_date = timezone.now()
            current_order.save()
            return render(request, 'order_module/payment_result.html', {
                'success': f'تراکنش شما با کد پیگیری {ref_str} با موفقیت انجام شد'
            })
        elif bodyResponse == 101:
            return render(request, 'order_module/payment_result.html', {
                'info': 'این تراکنش قبلا ثبت شده است'
            })


        # req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        # if len(req.json()['errors']) == 0:
        #     t_status = req.json()['data']['code']
        #     if t_status == 100:
        #         current_order.is_paid = True
        #         current_order.payment_date = time.time()
        #         current_order.save()
        #         ref_str = req.json()['data']['ref_id']
        #         return render(request, 'order_module/payment_result.html', {
        #             'success': f'تراکنش شما با کد پیگیری {ref_str} با موفقیت انجام شد'
        #         })
        #     elif t_status == 101:
        #         return render(request, 'order_module/payment_result.html', {
        #             'info': 'این تراکنش قبلا ثبت شده است'
        #         })
            # else:
            #     return HttpResponse('Transaction failed.\nStatus: ' + str(
            #         req.json()['data']['message']
            #     ))
            #     return render(request, 'order_module/payment_result.html', {
            #         'error': str(req.json()['data']['message'])
            #     })
        # else:
        #     e_code = req.json()['errors']['code']
        #     e_message = req.json()['errors']['message']
        #     # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        #     return render(request, 'order_module/payment_result.html', {
        #         'error': e_message
        #     })
    else:
        return render(request, 'order_module/payment_result.html', {
            'error': 'پرداخت با خطا مواجه شد / کاربر از پرداخت ممانعت کرد'
        })
