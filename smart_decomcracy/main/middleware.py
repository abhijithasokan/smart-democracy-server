import time
from importlib import import_module

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


import json

class MapJSONToSession(MiddlewareMixin):

	def process_request(self, request):
		if len(request.body)!=0:
			request.is_mobile = True
			print(request.body)
			request.POST = json.loads(request.body)
			x = request.POST.get('session_id',None)
			if x:
				print("Yep")
				request.COOKIES[settings.SESSION_COOKIE_NAME] = x
		print(request.COOKIES.get(settings.SESSION_COOKIE_NAME,None))
		return None


		# session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
		# request.session = self.SessionStore(session_key)

	# def process_view(self,):
	# 	pass


	def process_response(self, request, response):
		response['Access-Control-Allow-Origin'] = '*'
		return response
