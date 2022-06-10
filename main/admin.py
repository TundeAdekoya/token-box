from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([
    Account,
    Transfer,
    Withdraw,
    Deposit,
    check_balance
])