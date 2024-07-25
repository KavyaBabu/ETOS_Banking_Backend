from django.urls import path

from . import views

urlpatterns = [
    path('token/', views.GetToken.as_view()),
    path('refresh-token/', views.RefreshToken.as_view()),
    path('revoke-token/', views.RefreshToken.as_view()),
    # path('token/', views.token),
    # path('token/refresh/', views.refresh_token),
    # path('token/revoke/', views.revoke_token),
]