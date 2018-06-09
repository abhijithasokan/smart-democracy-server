from django.shortcuts import render

from django.http import JsonResponse
# Create your views here.
import os
from .models import User





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
		return old_view(request)
	return new_view





def getSessionId(request):
	request.session['sd']='asd'
	request.session.save()
	return JsonResponse({'sessionid': request.session.session_key})

def check(request):
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
			'sessionid': request.session.session_key,
			'success' : True,
			})
		return res


# def gitHook(request):
# 	os.system("git pull")


@isLoggedIn
def register(request):
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
			'sessionid': request.session.session_key,
			'success' : True,
			})
		