from rest_framework import serializers
from  .models import Account, Transfer, Withdraw, Deposit, check_balance


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['select_token','cash_amount', 'token_amount', 'account_no_transferred','reference' ]

class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = ['select_token','cash_amount', 'token_amount' ]

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = '__all__'

class Check_balanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = check_balance
        fields = '__all__'

