import random
import string


from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import User, SetOtp, ResetPasswordOTP 
from .serializers import UserSerializer, AdminSerializer, GetUserSerializer, UserProfileSerializer, ChangePasswordSerializer, ResetPasswordOTPSerializer, ConfirmResetOtpSerializer, ResetPasswordSerializer, LoginSerializer
from .signals import NewOtpSerializer, OTPVerifySerializer
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.signals import user_logged_in

# Create your views here.
class AddUser (generics.CreateAPIView):
    serializer_class = UserSerializer
    def AddUser(request):
        """Allows users to sigup on TokenBox"""
        if request.method == 'POST':
            serializer =  UserSerializer(data = request.data)
            if serializer.is_valid():
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
                user = User.objects.create(**serializer.validated_data, role='user')

                serializer = UserSerializer(user)

                data = {
                    'status' : True,
                    'message' : 'Successful',
                    'data' : serializer.data,
                }

                return Response(data, status = status.HTTP_201_CREATED)

            else:
                data = {
                    'status' :  False,
                    'message' : 'Unsuccessful',
                    'error' : serializer.errors,
                }

                return Response(data, status = status.HTTP_400_BAD_REQUEST)


class GetUser (generics.RetrieveAPIView):
    serializer_class = UserSerializer
    def GetUser(request):
        if request.method == 'GET':
            user = User.objects.filter (role = 'user', is_active = True)
            serializer = UserSerializer(user, many = True) 
            data = {
                'status' : True,
                'message' : 'Successful',
                'data' : serializer.data,
            }

            return Response (data, status=status.HTTP_200_OK)



class AddAdmin (generics.CreateAPIView):
    serializer_class = AdminSerializer
    def AddAdmin(request):
        """Allows super admin to add admin"""
        if request.method == 'POST':
            serializer = AdminSerializer(data = request.data)
            if serializer.is_valid():
                password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(8))
                serializer.validated_data['password'] = password
                user = User.objects.create(**serializer.validated_data, is_admin=True, is_active=True, role='admin')

                serializer = UserSerializer(user)
                data = {
                    'status' : True,
                    'message' : 'Successful',
                    'data' : serializer.data,
                }

                return Response(data, status = status.HTTP_201_CREATED)

            else:
                data = {
                    'status' : False,
                    'message':'Unsuccessful',
                    'error' : serializer.errors,
                }

                return Response (data, status = status.HTTP_400_BAD_REQUEST)

class GetAdmin (generics.ListAPIView):
    queryset = User.objects.filter(admin=True, active=True)
    serializer_class = AdminSerializer
 

class ListUserDetail (generics.ListAPIView):

    """Allows the logged in user to view their profile, edit or deactivate account. Do not use this view for changing password or resetting password"""

    queryset = User.objects.all()
    serializer_class = GetUserSerializer

class GetUserDetail (generics.UpdateAPIView):

    """Allows the admin to view user profile or deactivate user's account. """

    queryset = User.objects.all()
    serializer_class = GetUserSerializer

# OTP
class OtpReset (generics.CreateAPIView):
    serializer_class = NewOtpSerializer
    def OtpReset(request):
        if request.method == 'POST':
            serializer = NewOtpSerializer(data = request.data)
            if serializer.is_valid():
                data = serializer.get_new_otp()
                return Response (data, status = status.HTTP_200_OK)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class OtpVerification(generics.CreateAPIView):
    serializer_class = OTPVerifySerializer
    def OtpVerification(request):
       if request.method == 'POST':
           serializer = OTPVerifySerializer(data = request.data)
           if serializer.is_valid():
               data = serializer.verify_otp()

               return Response(data, status = status.HTTP_200_OK)
           else:
                return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPassword(generics.CreateAPIView):
    serializer_class = ResetPasswordOTPSerializer
    def ForgotPassword(request):
        if request.method == 'POST':
            serializer = ResetPasswordOTPSerializer (data = request.data)
            if serializer.is_valid():
                data = serializer.get_otp()
                return Response(data, status=status.HTTP_200_OK)


class ConfirmPassword(generics.CreateAPIView):
    serializer_class = ConfirmResetOtpSerializer
    def ConfirmPassword(request):
        if request.method == 'POST':
            serializer = ConfirmResetOtpSerializer (data = request.data)
            if serializer.is_valid():
                data  = serializer.verify_otp()
                return Response( data, status = status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTPP_400_BAD_REQUEST)