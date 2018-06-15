import time
from importlib import import_module

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


import json

class MapJSONToSession(MiddlewareMixin):
	def process_request(self, request):
		if len(request.POST)==0 and len(request.body)!=0:
			request.is_mobile = True
			request.POST = json.loads(request.body)
			session_id = request.POST.get('session_id',None)
			if session_id:
				print("Yep")
				request.COOKIES[settings.SESSION_COOKIE_NAME] = session_id
		print(request.COOKIES.get(settings.SESSION_COOKIE_NAME,None))
		return None

	def process_response(self, request, response):
		response['Access-Control-Allow-Origin'] = '*'
		return response
