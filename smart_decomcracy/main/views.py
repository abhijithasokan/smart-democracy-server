from django.shortcuts import render

from django.http import JsonResponse
# Create your views here.
import os
from .models import User, MLA, Issue, Solution,Poll, Option





def isLoggedIn(old_view):
	def new_view(request):
		try:
			user_id = request.session.get('user',None)
		except:
			user_id = None

		if user_id == None:
			return JsonResponse({
				'success' : False,
			})

		if 'official' in request.session:
			return old_view(request,MLA.objects.get(user_id=user_id))
		else:
			print("User who is loggedIn: ",user_id)
			return old_view(request,User.objects.get(user_id=user_id))
	return new_view





def getSessionId(request):
	request.session['sd']='asd'
	request.session.save()
	return JsonResponse({'sessionid': request.session.session_key})



@isLoggedIn
def check(request,user):
	return JsonResponse({'ok': True})

'''
{
	'user_id':
	'password':
}
'''

def login(request):
	user_id = request.POST['user_id']
	password = request.POST['password']

	user = User.getUser(user_id,password)
	print(user)
	if user == None:
		return JsonResponse({
				'success' : False,
			})

	else:
		request.session['user'] = user.user_id
		request.session.save()
		res =  JsonResponse({
			'session_id': request.session.session_key,
			'success' : True,
			})
		return res


# def gitHook(request):
# 	os.system("git pull")


def register(request):
	if 'official' in request:
		# continue
		user = MLA.create(
			name = request.POST['name'],
			user_id = request.POST['user_id'],
			password = request.POST['password'],
			constituency_name = request.POST['constituency_name']
		)
		if user == None:
			return JsonResponse({
					'success' : False,
				})
		else:
			request.session['user'] = user.user_id
			request.session['official'] = True
			request.session.save()
			return  JsonResponse({
				'session_id': request.session.session_key,
				'success' : True,
				})
	else:
		user = User.create(
			name = request.POST['name'],
			voter_id = request.POST['voter_id'],
			user_id = request.POST['user_id'],
			password = request.POST['password'],
			constituency_name = request.POST['constituency_name']
		)
		if user == None:
			return JsonResponse({
					'success' : False,
				})
		else:
			request.session['user'] = user.user_id
			request.session.save()
			return  JsonResponse({
				'session_id': request.session.session_key,
				'success' : True,
				})




#============ISSUES
		

@isLoggedIn
def getIssues(request,user):
	return JsonResponse({
			'data' : Issue.getIssues(user)
		})

@isLoggedIn
def createIssue(request,user):
	#x = (cls,heading,description,creator)
	x = Issue.create(heading = request.POST['heading'],
		description = request.POST['description'],
		creator = user
	)
	return JsonResponse({
			'success' : True
		})

@isLoggedIn
def upvote(request,user):
	item = request.POST['item']
	id = request.POST['id']
	if item == 'issue':
		Issue.objects.get(issue_id=id).upvote()
	elif item == 'solution':
		Issue.objects.get(issue_id=id).upvote()



@isLoggedIn
def createSolution(request,user):
	x = Solution.create(heading = request.POST['heading'],
		description = request.POST['description'],
		issue_id = request.POST['issue_id'],
		creator=user
	)
	return JsonResponse({
			'success' : True
		})
 


@isLoggedIn
def getSolutions(request,user):
	issue_id = request.POST['issue_id']
	return JsonResponse({
			'data' : Solution.getSolutions(issue=issue_id)
		})


# {
# 'data' : [
# 	{
# 		'upvotes': 3,
# 		'downvotes' : 1,
# 		'heading' : 'issue1',
# 		'description' : 'this is a description',
# 		'official' : False,
# 		'creator' : 'Suraj',
# 	},
# 	{
# 		'upvotes': 5,
# 		'downvotes' : 2,
# 		'heading' : 'issue 2',
# 		'description' : 'this is a description hahahahahaha',
# 		'official' : True,
# 		'creator' : 'Asif',
# 	},

# ]
# }

#


#================= Poll

'''
{
	'poll_id : '',
	'
}
'''

@isLoggedIn
def vote(request,user):
	poll_id = request.POST['poll_id']
	option_num = request.POST['option_id']

	p = Poll.objects.get(poll_id=poll_id)
	p.vote(option_num)
	p.save()


@isLoggedIn
def createPoll(request,user):
	print("createPoll: ",request.POST['option'])
	options = request.POST['option'].strip()[1:-1].split(', ')

	# request.POST['description'] = 'good des'
	# request.POST['heading'] = 'nICE HEADING'

	x = Poll.create(
		heading = request.POST['heading'],
		description = request.POST['description'],
		creator=user,
		options = options,
	)

	return JsonResponse({
			'success' : True
		})




@isLoggedIn
def getPolls(request,user):
	return JsonResponse({
			'data' : Poll.getPolls(user),
		})	

@isLoggedIn
def getPollResult(request,user):
	return JsonResponse({
			'data' : Poll.objects.get(poll_id=request.POST['poll_id']).getPollResult(),
		})	
