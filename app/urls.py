from django.urls import path,include, re_path
from .views import *
urlpatterns = [
    path('admin/bankaccount', UserRegistrationView.as_view(),name = "user_registration"),
    path('account/login',MyTokenObtainPairView.as_view(), name='login'),
    path('account/balance/<slug:account_no>',AccountView.as_view(),name="_balace"),
    path('accounts/transactions',TransactionView.as_view(),name= "transactions"),
    path('account/transaction/transfer',TransactionView.as_view(),name = "transfer")
    # re_path(r'^api/model/'
]
