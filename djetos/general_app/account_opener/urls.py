from django.urls import include
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers

from .view import account_opener_views


urlpatterns = [
    path('open_account/', account_opener_views.account_opener_view,name="account_opening"),
    path('activate_email/<str:activation_key>/', account_opener_views.activate_email, name='verify-email'),
    path('verify_email/', account_opener_views.verify_email_status, name='verify_email_status')
]
