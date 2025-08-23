from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Placeholder views for accounts app

class RegisterView(TemplateView):
    """User registration view - placeholder"""
    template_name = 'accounts/register.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Register for Onam Celebration'
        return context


class LoginView(TemplateView):
    """User login view - placeholder"""
    template_name = 'accounts/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Login to Onam Celebration'
        return context


class LogoutView(TemplateView):
    """User logout view - placeholder"""
    template_name = 'accounts/logout.html'


class PhoneVerificationView(TemplateView):
    """Phone verification view - placeholder"""
    template_name = 'accounts/verify_phone.html'


class ResendCodeView(APIView):
    """Resend verification code - placeholder"""
    def post(self, request):
        return Response({'message': 'Code resent (placeholder)'}, status=status.HTTP_200_OK)


class ProfileView(TemplateView):
    """User profile view - placeholder"""
    template_name = 'accounts/profile.html'


class EditProfileView(TemplateView):
    """Edit profile view - placeholder"""
    template_name = 'accounts/edit_profile.html'


class ChangePasswordView(TemplateView):
    """Change password view - placeholder"""
    template_name = 'accounts/change_password.html'


class PasswordResetView(TemplateView):
    """Password reset view - placeholder"""
    template_name = 'accounts/password_reset.html'


class PasswordResetConfirmView(TemplateView):
    """Password reset confirm view - placeholder"""
    template_name = 'accounts/password_reset_confirm.html'


class CheckPhoneAPIView(APIView):
    """Check phone number API - placeholder"""
    def post(self, request):
        return Response({'available': True}, status=status.HTTP_200_OK)


class VerifyCodeAPIView(APIView):
    """Verify code API - placeholder"""
    def post(self, request):
        return Response({'verified': True}, status=status.HTTP_200_OK)
