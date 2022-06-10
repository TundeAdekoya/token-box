from select import select
from django.db import models
from accounts.models import User

bank_type = [('select' ,'Select'), ('zenith Bank', 'Zenith bank'), ('gt bank', 'GT Bank'), ('eco Bank', 'Eco bank'), ('uba Bank', 'UBA bank'), ('polaris bank', 'Polaris Bank'), ('standard chartered bank', 'Standard Chartered Bank'), ('keystone bank', 'Keystone Bank'), ('access bank', 'Access Bank'), ('sterling bank', 'Sterling Bank')]

token_type = [('select','Select'),('nft','NFT'),('cryptocurrency', 'Cryptocurrency'),('all', 'All'), ('cash','Cash')]

select = [('cryptocurrency', 'Cryptocurrency'), ('nft','NFT'), ('none', 'None')]

class Account(models.Model):

    # Represents Bank account

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    bank_name = models.CharField(max_length=50, choices=bank_type, default='select')
    token = models.CharField(max_length=50, choices=token_type, default='select')
    cash_avaliable = models.FloatField(blank=True,null=True)
    token_avaliable = models.FloatField(blank=True,null=True)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = "User's Account"



class Transfer(models.Model):
    bank_name = models.CharField(max_length=50, choices=bank_type, default='select')
    select_token = models.CharField(max_length=50, choices=select, blank=True,null=True)
    cash_amount = models.FloatField(blank=True,null=True)
    token_amount = models.FloatField(blank=True,null=True)
    account_no_transferred = models.IntegerField(blank=True,null=True)
    reference = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.cash_amount} {self.token_amount} has been transferred to {self.account_no_transferred}."

    class Meta:
        verbose_name = 'Transfer'


class Withdraw(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    select_token = models.CharField(max_length=50, choices=select, blank=True,null=True)
    cash_amount = models.FloatField(blank=True,null=True)
    token_amount = models.FloatField(blank=True,null=True)

    def __str__(self):
        return f"{self.cash_amount} {self.token_amount} has been withdrawn from your account."

    class Meta:
        verbose_name = 'Withdraw'



class Deposit(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.amount} has been deposited to {self.account}."

    class Meta:
        verbose_name = 'Deposit'



class check_balance(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def json_object(self):
        return{
            'account': self.token_avaliable,
            'account': self.cash_avaliable
        }

    def __str__(self):
        return f"You have!" + self.json_object() + "in your" + {self.account}

    class Meta:
        verbose_name = 'Check Balance'

