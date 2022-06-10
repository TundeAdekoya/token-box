from django.urls import  path
from .views import AddAccount, AccountDetail, AccountList, TransferList, AddTransfer, TransferDetail, AddWithdraw, WithdrawList, WithdrawDetail, AddDeposit, DepositDetail, DepositList, CheckBalance, CheckBalanceDetail

urlpatterns = [
    path('account/add_account/', AddAccount.as_view()),
    path('account/all_account/', AccountList.as_view()),
    path('account/<int:pk>/', AccountDetail.as_view()),

    path('transfer/make_transfer/', AddTransfer.as_view()),
    path('transfer/all_transfer/', TransferList.as_view()),
    path('transfer/<int:pk>/', TransferDetail.as_view()),

    path('withdraw/make_withdraw/', AddWithdraw.as_view()),
    path('withdraw/all_withdraw/', WithdrawList.as_view()),
    path('withdraw/<int:pk>/', WithdrawDetail.as_view()),

    path('deposit/make_deposit/', AddDeposit.as_view()),
    path('deposit/all_deposit/', DepositList.as_view()),
    path('deposit/<int:pk>/', DepositDetail.as_view()),

    path('balance/check_balance/', CheckBalance.as_view()),
    path('balance/<int:pk>/', CheckBalanceDetail.as_view()),

]
