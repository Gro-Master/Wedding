from django.urls import path
from common import views
from django.shortcuts import render

urlpatterns = [
    path('', views.MobileRedirectView.as_view(), name='home'),
    path('unlock/', views.UnlockView.as_view(), name='unlock'),
    path('main/', views.Invitation.as_view(), name='invitation'),
]