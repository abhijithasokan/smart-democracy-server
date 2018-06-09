from django.urls import path
from .views import check, getSessionId, login

urlpatterns = [
    path('check', check ),
    path('getSessionId', getSessionId ),
    path('login', login)
]