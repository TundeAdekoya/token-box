from email import message
from accounts.serializers import UserSerializer
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
import pyotp
from .models import SetOtp, ResetPasswordOTP
from config import settings
from rest_framework import serializers
from django.template.loader import render_to_string

totp = pyotp.TOTP('base32secret3232', interval=300)

domain = 'tokenbox.com'

url = '#'

User = get_user_model()


@receiver(post_save, sender=ResetPasswordOTP)
def password_reset_token_created(sender, instance, created, *args, **kwargs):
    if created:
        code = instance.code

        msg_html = render_to_string('forgot_password_otp.html', {'first_name':str(instance.user.first_name).title(), 
        'code':code})

        message = 'Hello {},\n\nYou are receiving this message because you or someone else has requested to reset the password of this account. \nYour reset passcode is {}. \nIf you did not request this please ignore this e-mail and your password would remain unchanged. OTP expires in 5 minutes.\nRegards,\nTokenBox Team'.format(instance.user.first_name, code)
        
        send_mail(
            subject ="Reset Password OTP for TokenBox",
            message = message,
            html_message = msg_html,
            from_email = 'TokenBox  Supposrt <noreply@TokenBox Bank.com>',
            recipient_list = [instance.email])

@receiver(post_save, sender=User)
def send_otp(sender, instance, created, **kwargs):
    if  created and instance.email == 'user':
        code = totp.now()
        print(code)
        subject = "Account Verification For TokenBox"

        message = f"""Hello {str(instance.first_name).titile()}.
        Thank you for Signing Up!
        Complete your verification on Token Box with the OTP below:

        {code}

        Expires in 5 minutes!

        Thank you,
        Token Box
        
        """

        msg_html = render_to_string('signup_email.html', {
            'first_name' : str(instance.first_name).title(),
            'code': code,
            'url':url
        })  

        email_from = settings.Common.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail(subject, message, email_from, recipient_list, html_message=msg_html)

        SetOtp.objects.create(code=code, user=instance)
        return 


class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length = 6)

    def verify_otp(self):
        otp = self.validated_data['otp']

        if SetOtp.objects.filter(code=otp).exists():
            try:
                otp = SetOtp.objects.get(code=otp)
            except Exception:
                SetOtp.objects.filter(code=otp).delete()
                raise serializers.ValidationError(detail='Cannot verify otp. Please Again')

            if totp.verify(otp.code):
                if otp.user.is_active == False:
                    otp.user.is_active = True
                    otp.user.save()

                    all_otps = SetOtp.objects.filter(user = otp.user)
                    all_otps.delete()

                    serializer = UserSerializer(otp.user)
                    return {'message': 'Verification Complete', 'data':serializer.data}
                else:
                    raise serializer.ValidationError(detail='The User with this OTP has been verified')

            else:
                raise serializer.ValidationError(detail='OTP expired')

        else:
            raise serializers.ValidationError(detail='Invalid OTP')


class NewOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def get_new_otp(self):
        try:
            user = User.objects.get(email=self.validated_data['email'], is_active= False)
        except User.DoesNotExist:
            raise serializers.ValidationError(detail = 'kindly confirm that the email is correct and is verified.')

        code = totp.now()
        print(code)
        SetOtp.objects.create(code=code, user=user)
        subject = 'New OTP for TokenBox'
        message = f"""Hello! {str(user.first_name).title()}.
                    Complete your verification on TokenBox with the OTP below:
                    
                    {code}
                    
                    Expires in 5 minutes!
                    
                    Thank you,
                    TokenBox
                    """

        msg_html = render_to_string('new_otp_html', 
                                    {'first_name': str(user.first_name).title(),
                                    'code' : code,
                                    'url': url })

        email_from = settings.Common.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, email_from, recipient_list, html_message=msg_html)

        return {'message': 'Kindly check your email for OTP.'}