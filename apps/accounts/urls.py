from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Phone verification
    path('verify-phone/', views.PhoneVerificationView.as_view(), name='verify_phone'),
    path('resend-code/', views.ResendCodeView.as_view(), name='resend_code'),
    
    # Profile management
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    
    # Password management
    path('password/change/', views.ChangePasswordView.as_view(), name='change_password'),
    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # API endpoints
    path('api/check-phone/', views.CheckPhoneAPIView.as_view(), name='api_check_phone'),
    path('api/verify-code/', views.VerifyCodeAPIView.as_view(), name='api_verify_code'),
]
