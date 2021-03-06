from django.urls import path
from .views import login, register, createIssue, getIssues, createIssue, vote
from .views import createPoll, getPolls, createSolution, getSolutions, upvote, downvote, getIssuesPrev

urlpatterns = [
    path('login', login), #set
    path('register', register), #set
    
    path('upvote',upvote),	#set
    path('downvote',downvote),	#set

    path('createIssue', createIssue), #set
    path('getIssues',getIssues), #set
    path('getIssuesPrevious',getIssuesPrev),		#set

    path('createSolution',createSolution), #set
    path('getSolutions',getSolutions), #set
    #path(),

    path('createPoll',createPoll), #set
    path('vote',vote),			#set		
    path('getPolls',getPolls),	#set

]