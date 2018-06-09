from django.urls import path
from .views import check, getSessionId, login, register, createIssue, getIssues, createIssue, vote, createPoll

urlpatterns = [
    path('check', check ),
    path('getSessionId', getSessionId ),
    path('login', login),
    path('register', register),
    
    path('createIssue', createIssue),
    path('getIssues',getIssues),


    path('createPoll',createPoll),
    path('vote',vote),
]