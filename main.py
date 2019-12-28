import pycurl
from io import BytesIO
import re
import random
import json

class ProxyChecker:
	def __init__(self):
		self.ip = self.get_ip()
		self.proxy_judges = self.get_proxy_judges()

	def get_ip(self):
		return '<ip>'

	def get_proxy_judges(self):
		return [
			'http://proxyjudge.us/azenv.php',
			'http://mojeip.net.pl/asdfa/azenv.php'
		]

	def send_query(self, proxy, url=None):
		response = BytesIO()

		c = pycurl.Curl()

		c.setopt(c.URL, url or random.choice(self.proxy_judges))
		c.setopt(c.WRITEDATA, response)
		c.setopt(c.TIMEOUT, 5)

		c.setopt(c.SSL_VERIFYHOST, 0)
		c.setopt(c.SSL_VERIFYPEER, 0)

		if proxy:
			c.setopt(c.PROXY, proxy)

		# Perform request
		try:
			c.perform()
		except Exception as e:
			# print(e)
			return False

		# Return false if status code is not 200 
		if c.getinfo(c.HTTP_CODE) != 200:
			return False
			
		# Calculate request timeout
		timeout = round(c.getinfo(c.CONNECT_TIME) * 1000)

		# Decode response content
		response = response.getvalue().decode('iso-8859-1')

		return {
			'timeout': timeout,
			'response': response
		}

	def parse_anonymity(self, r):		
		if self.ip in r:
			return 'Transparent'
		
		privacy_headers = [
			'VIA',
			'X-FORWARDED-FOR',
			'X-FORWARDED',
			'FORWARDED-FOR',
			'FORWARDED-FOR-IP',
			'FORWARDED',
			'CLIENT-IP',
			'PROXY-CONNECTION'
		]

		if any([header in r for header in privacy_headers]):
			return 'Anonymous'

		return 'Elite'

	def get_country(self, ip):
		r = self.send_query(False, url='https://ip2c.org/' + ip)

		if r and r['response'][0] == '1':
			r = r['response'].split(';')
			return [r[3], r[1]]
		
		return ['-', '-']

	def check_proxy(self, proxy, check_country=True):
		protocols = {}
		timeout = 0

		# Test proxy for each protocol
		for protocol in ['http', 'socks4', 'socks5']:
			r = self.send_query(protocol + '://' + proxy)

			# Check if the request failed
			if not r:
				continue

			protocols[protocol] = r
			timeout += r['timeout']

		# Check if the proxy failed all tests
		if (len(protocols) == 0):
			return False

		# Get country
		if check_country:
			country = self.get_country(proxy.split(':')[0])


		# Check anonymity
		anonymity = self.parse_anonymity(protocols[random.choice(list(protocols.keys()))]['response'])

		# Check anonymity
		timeout = timeout // len(protocols)

		if check_country:
			return {
				'country': country[0],
				'country_code': country[1],
				'protocols': list(protocols.keys()),
				'anonymity': anonymity,
				'timeout': timeout
			}

		return {
			'protocols': list(protocols.keys()),
			'anonymity': anonymity,
			'timeout': timeout
		}
