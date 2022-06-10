from django.shortcuts import get_object_or_404, render
from .permissions import isAuthenticated
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

# import accounts.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
# Create your views here.
from .models import Account, Transfer, Withdraw, Deposit, check_balance
from .serializers import AccountSerializer, TransferSerializer, WithdrawSerializer, DepositSerializer, Check_balanceSerializer

class AccountList(generics.ListCreateAPIView, LoginRequiredMixin):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class AddAccount(generics.CreateAPIView, LoginRequiredMixin):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def post(self, request, pk, format=None):
        print("========== Welcome to TokenBox ==========")
        account = get_object_or_404(Account, pk=pk)
        account.user.add(request.user)
        account_no = random.randint(7770000,7779999)            
        return Response ({f"Account Created, Your account number is {account_no}": True})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
        

class AccountDetail(generics.RetrieveUpdateDestroyAPIView, LoginRequiredMixin):
    permission_classes = (permissions.IsAdminUser,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

# Transfer View

class TransferList(generics.ListCreateAPIView, LoginRequiredMixin):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class AddTransfer(generics.CreateAPIView, LoginRequiredMixin):
    permission_classes = (permissions.IsAuthenticated,) 
    def post(self, request, pk, format=None):
        transfer = get_object_or_404(Transfer, pk=pk)
        transfer.token_amount.add(request.account_no_transferred)
        transfer.cash_amount.add(request.account_no_transferred)
        if transfer.cash_amount in transfer.account_no_transferred:
            'Transfer Successful'
        elif transfer.cash_amount not in transfer.account_no_transferred:
            'Transfer Failed'
        elif  transfer.token_amount in transfer.account_no_transferred:
            'Transfer Successful'    
        elif  transfer.token_amount not in transfer.account_no_transferred:
            'Transfer Failed'

        return Response ({"Transfer Successful": True})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class TransferDetail(generics.RetrieveUpdateDestroyAPIView, LoginRequiredMixin):
    permission_classes = (permissions.IsAdminUser,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


# Withdraw View

class WithdrawList(generics.ListCreateAPIView, LoginRequiredMixin):
    permission_classes = (permissions.IsAdminUser,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Withdraw.objects.all()
    serializer_class = WithdrawSerializer

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class AddWithdraw(generics.CreateAPIView, LoginRequiredMixin):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, pk, format=None):
        withdraw = get_object_or_404(Withdraw, pk=pk)
        withdraw.cash_amount.remove(request.account)
        withdraw.token_amount.remove(request.account)
        if withdraw.cash_amount in withdraw.account:
            'Withdraw Successful'
        elif withdraw.cash_amount not in withdraw.account:
            'Withdraw Failed'
        elif  withdraw.token_amount in withdraw.account:
            'Withdraw Successful'   
        elif  withdraw.token_amount not in withdraw.account:
            'Withdraw Failed'

        return Response ({'Withdraw Successful': True})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class WithdrawDetail(generics.RetrieveUpdateDestroyAPIView, LoginRequiredMixin):
    permission_classes = (permissions.IsAdminUser,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Withdraw.objects.all()
    serializer_class = WithdrawSerializer

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    


# Deposit View

class DepositList(generics.ListCreateAPIView, LoginRequiredMixin):
    permission_classes = (permissions.IsAdminUser,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class AddDeposit(generics.CreateAPIView, LoginRequiredMixin):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, pk, format=None):
        deposit = get_object_or_404(Deposit, pk=pk)
        deposit.cash_amount.remove(request.account)
        deposit.token_amount.remove(request.account)
        if deposit.cash_amount in deposit.account:
            'Deposit Successful'
        elif deposit.cash_amount not in deposit.account:
            'Deposit Failed'
        elif  deposit.token_amount in deposit.account:
            'Deposit Successful'   
        elif  deposit.token_amount not in deposit.account:
            'Deposit Failed'

        return Response ({'Deposit Successful': True})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class DepositDetail(generics.RetrieveUpdateDestroyAPIView, LoginRequiredMixin):
    permission_classes = (permissions.IsAdminUser,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    
# Balance View

class CheckBalance(generics.ListCreateAPIView, LoginRequiredMixin):
    permission_classes = (permissions.IsAdminUser,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = check_balance.objects.all()
    serializer_class = Check_balanceSerializer

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class CheckBalanceDetail(generics.RetrieveUpdateDestroyAPIView, LoginRequiredMixin):
    permission_classes = (permissions.IsAdminUser,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)    
    queryset = check_balance.objects.all()
    serializer_class = Check_balanceSerializer

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)



    