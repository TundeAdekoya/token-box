import uuid
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django_countries.fields import CountryField
from django.core.validators import RegexValidator

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None): 
            if not email:
                raise ValueError('TokenBox users must have an email address')
            user = self.model(
                email = self.normalize_email(email)
            )
            user.set_password(password)
            user.save(using=self._db)
            return user



class User(AbstractBaseUser):
    token_box_acc_type = [ ('Select','select'), ('Savings','savings'), ('Current','current') ]

    # Represent Users Information 
    phone_regex = RegexValidator(regex=r'^\+?234?\d{9,17}$', message="Phone number must be entered in the format: '+2341234567890'.")
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    email = models.EmailField(max_length=300)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) #validators should be a list

    active = models.BooleanField(default=True) #user can login 
    staff = models.BooleanField(default=False) #check if user is staff
    admin = models.BooleanField(default=False)  #check if user is admin

    first_name = models.CharField(max_length=40)
    last_name =  models.CharField(max_length=40)
    date_of_birth = models.DateField((""), auto_now=False, auto_now_add=False)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=300)
    nationality = CountryField()
    address =   models.CharField(max_length=500)
    account_type = models.CharField(max_length=10, choices = token_box_acc_type, default='Select')
    date_created = models.DateTimeField(auto_now_add=True)
    national_identification_number = models.IntegerField( blank=True,null=True)
    bank_verification_number = models.IntegerField( blank=True,null=True)
    mothers_maiden_name = models.CharField(max_length=40)

    USERNAME_FIELD = 'email' #username
    REQUIRED_FIELDS = ['first_name','last_name', 'date_of_birth', 'address', 'account_type', 'national_identification_number', 'bank_verification_number', 'mothers_maiden_name' ]

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    objects = UserManager()

    def __str__(self) :
        return self.email

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name
    
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin


class SetOtp(models.Model):
    otp_code = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.otp_code


class ResetPasswordOTP(models.Model):
    opt_code = models.CharField(max_length=6)
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.otp_code + 'for' + self.email
  

