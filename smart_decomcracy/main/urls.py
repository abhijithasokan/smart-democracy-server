from django.urls import path
from .views import check, getSessionId, login, register

urlpatterns = [
    path('check', check ),
    path('getSessionId', getSessionId ),
    path('login', login),
    path('register', register),
]