from django.urls import path
from .views import register_user, login_user,add_transaction, get_transactions,  delete_transaction,update_transaction

from rest_framework_simplejwt.views import (
   TokenObtainPairView,
   TokenRefreshView,
)

urlpatterns = [

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register', register_user, name='register_user'),
    path('login', login_user, name='login_user'),
    path('add-transaction', add_transaction, name='add_transaction'),
    path('get-transactions', get_transactions, name='get_transactions'),
    path('delete-transaction/<int:id>', delete_transaction, name='delete_transaction'),
    path('update-transaction/<int:id>', update_transaction, name='update_transaction'),

]