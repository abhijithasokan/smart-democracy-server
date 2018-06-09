from django.urls import path
from .views import check, getSessionId, login, register, createIssue, getIssues, createIssue, vote
from .views import createPoll, getPolls, createSolution, getSolutions

urlpatterns = [
    path('check', check ),
    path('getSessionId', getSessionId ),
    path('login', login), #set
    path('register', register), #set
    
    path('createIssue', createIssue), #set
    path('getIssues',getIssues), #set

    path('createSolution',createSolution), #set
    path('getSolutions',getSolutions),

    path('createPoll',createPoll), #set
    path('vote',vote),
    path('getPolls',getPolls),
]