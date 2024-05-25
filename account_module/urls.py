from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register_page'),
    path('registerdetails/', views.RegisterdetailsView.as_view(), name='registerdetails_page'),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_page'),
    path('forget-pass/', views.ForgetPasswordView.as_view(), name='forget_password_page'),
    path('reset-pass/<active_code>', views.ResetPasswordView.as_view(), name='reset_password_page'),
    path('activate-account/<email_active_code>', views.ActivateAccountView.as_view(), name='activate_account'),


    path('order_history/', views.order_history_view, name='order_history'),
    path('order_details/<int:order_id>/', views.order_details_view, name='order_details'),

    
]
