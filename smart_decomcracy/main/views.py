from django.shortcuts import render

from django.http import JsonResponse
# Create your views here.

from .models import User


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
		res =  JsonResponse({'sessionid': request.session.session_key})
		return res
