from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, ResetPasswordOTP
from django.contrib.auth import password_validation
import pyotp

totp = pyotp.TOTP("JBSWY3DPEHPK3PXP", interval=300)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, allow_blank= True )

    class Meta:
        model = User 
        fields = ['id','first_name','last_name', 'email', 'phone_number', 'date_of_birth', 'password','image', 'nationality', 'address', 'account_type', 'date_created', 'national_identification_number', 'bank_verification_number', 'mothers_maiden_name' ] 

    def validate_password(self, value):
        try:
            password_validation.validate_password(value, self.instance)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, allow_blank= True )

    class Meta:
        model = User 
        fields = ['id','first_name','last_name', 'email', 'phone_number', 'date_of_birth', 'password','image', 'nationality', 'address','date_created', 'national_identification_number',  ] 

    def validate_password(self, value):
        try:
            password_validation.validate_password(value, self.instance)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

class GetUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User 
        fields = [ 'email', 'bank_verification_number'] 

    def validate_password(self, value):
        try:
            password_validation.validate_password(value, self.instance)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User 
        fields = [ 'first_name','last_name','email', 'bank_verification_number', 'account_type'] 

    def validate_password(self, value):
        try:
            password_validation.validate_password(value, self.instance)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=200)
    new_password = serializers.CharField(max_length=200)
    confirm_password = serializers.CharField(max_length=200)

    def check_password(self):
        if self.validated_data['new_password'] != self.validated_data['confirm_password']:
            raise serializers.ValidationError({"Error":"Enter maching Password"})
        return True

class ResetPasswordOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def get_otp(self):
        try:
            user = User.objects.get(email = self.validated_data['email'], is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError(detail='User not found')

        code = totp.now()

        ResetPasswordOTP.objects.create(code=code, email=self.validated_data['email'], user = user)

        return{'message': 'Check email for OTP'}


class ConfirmResetOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length = 6)
    email = serializers.EmailField()

    def verify_otp(self):
        code = self.validate_data['otp']
        email = self.validated_data['email']

        if ResetPasswordOTP.objects.filter(code=code, email=email).exists():
            try:
                otp = ResetPasswordOTP.objects.get(code=code, email=email)
            except Exception:
                ResetPasswordOTP.objects.filter(code=code, email=email).delete()
                raise serializers.ValidationError(detail = "Can't verify OTP. Try again")

            if otp.verify(otp.code):
                return {'message': 'success'}

            else:
                raise serializers.ValidationError(details="OTP has Expired")
            

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=3000)

    def reset_password(self):
        try:
            user = User.objects.get(email=self.validated_data['email'], is_active = True)
        except User.DoesNotExist:
            raise serializers.ValidationError(detail='Error Change Password')

        user.set_password(self.validated_data['password'])
        user.save()

        return {'message': 'Password reset complete'}


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length = 200)
