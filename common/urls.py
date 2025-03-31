from django.urls import path
from common import views
from django.shortcuts import render

urlpatterns = [
    path("", views.Invitation.as_view(), name='invitation'),
    # path('', lambda request: render(request, 'index.html'), name='home'),
]