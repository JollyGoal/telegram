from django.urls import path

from .views import *


urlpatterns = [
    path('v_t/', VerifiedTransactionsView.as_view()),
    path('profiles/', ProfilesView.as_view()),
    path('transactions_verified/', TransactionsVerifiedView.as_view()),
    path('transactions_not_verified/', TransactionsNotVerifiedView.as_view()),
]
