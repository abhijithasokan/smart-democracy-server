from urllib import request,parse
import re
import csv

headers = {
	'Accept-Language': 'en-US,en;q=0.8', 
	'Accept-Encoding': 'none', 
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 
	'Connection': 'keep-alive', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
	'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0.1; MotoG4 Build/MPI24.107-55) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.81 Mobile Safari/537.36'
}

url = 'http://electoralsearch.in/'
req = request.Request(url,headers=headers)
res = request.urlopen(req)


# csrf_token = re.search('csrftoken=(.*?);', res.headers['set-cookie']).group(1)
# encode_type = re.search('charset=([^;]*)', res.headers['content-type']).group(1)
# print(encode_type)
# headers['Cookie'] = 'csrftoken=%s'%csrf_token
# headers['X-CSRFToken'] = csrf_token

# _post_data = {
# 	'csrfmiddlewaretoken' : csrf_token,
# 	'searchby' : 'name',
# 	'value' : '',
# }

# post_data = parse.urlencode(_post_data).encode()

req = request.Request(url,headers=headers)
# rep = request.urlopen(req,data=post_data)

rep = request.urlopen(req)

page = rep.read().decode('utf8')#encode_type)

f = open('asd.html','w')
f.write(page)
f.close()

# data_required = re.findall(s,page,re.DOTALL)
# print(len(data_required))


# with open('dict.csv', 'w') as csv_file:
# 	for row in data_required:
# 		#print('%-08s %-030s %-040s %-030s %-012s'%row)
# 		csv_file.write('\n"%s","%s","%s","%s","%s"'%row)