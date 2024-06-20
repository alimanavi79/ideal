from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserPanelDashboardPage.as_view(), name='user_panel_dashboard'),
    path('change-pass', views.ChangePasswordPage.as_view(), name='change_password_page'),
    path('edit-profile', views.EditUserProfilePage.as_view(), name='edit_profile_page'),
    path('user-basket', views.user_basket, name='user_basket_page'),
    path('user-basket2', views.user_basket2, name='user_basket_page2'),
    path('my-shopping', views.MyShopping.as_view(), name='user_shopping_page'),
    path('my-shopping-detail/<order_id>', views.my_shopping_detail, name='user_shopping_detail_page'),
    path('remove-order-detail', views.remove_order_detail, name='remove_order_detail_ajax'),
    path('change-order-detail', views.change_order_detail_count, name='change_order_detail_count_ajax'),
    path('print-invoice/<int:order_id>/', views.print_invoice, name='print_invoice'),
    path('remove-discount-code/', views.remove_discount_code, name='remove_discount_code'),


    path('ajax/load-shahrestans/', views.load_shahrestans, name='ajax_load_shahrestans'),


]
