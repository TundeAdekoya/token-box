from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AddUser, GetUser, ListUserDetail, GetUserDetail, AddAdmin, GetAdmin, ForgotPassword, ConfirmPassword, OtpVerification, OtpReset

urlpatterns = [
    # users
    path('user/add_user/', AddUser.as_view()),
    path('user/all_user/', GetUser.as_view()),
    path('user/profile/', ListUserDetail.as_view()),
    path('user/<int:pk>/', GetUserDetail.as_view()),
    path('user/add_admin/', AddAdmin.as_view()),
   
    # auth 
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # password
    path('user/forgot_password/', ForgotPassword.as_view()),
    path('user/forgot_password/confirm_password/', ConfirmPassword.as_view()),

    path('otp/', OtpVerification.as_view()),
    path('otp/new/', OtpReset.as_view())
    
]
