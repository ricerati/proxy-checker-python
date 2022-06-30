from io import BytesIO
import json
import random
import re
import pycurl
from typing import Union
import certifi
class ProxyChecker:
    def __init__(self, timeout: int = 5000, verbose: bool = False):
        self.timeout = timeout
        self.verbose = verbose 
        self.proxy_judges = [
            'https://www.proxy-listen.de/azenv.php',
            'http://mojeip.net.pl/asdfa/azenv.php',
            'http://httpheader.net/azenv.php',
            'http://pascal.hoez.free.fr/azenv.php'
        ]

        self.ip = self.get_ip()
        
        # Checks
        if self.ip == "":
            print("ERROR: https://api.ipify.org is down. This module won't work")
            exit()

        self.check_proxy_judges()

    def change_timeout(self, timeout: int) -> None:
        '''
            Sets timeout for requests
            Args:
                :param timeout, int. Timeout in ms
        '''
        self.timeout = timeout

    def change_verbose(self, value: bool) -> None:
        '''
            Sets verbose for curl
        '''
        self.verbose = value

    def check_proxy_judges(self) -> None:
        '''
            This proxy checks several urls to get the proxy availability. These are the judges.
            There are several in this module. However, they can be nonoperational. This function 
            removes the one not operative.
        '''
        checked_judges = []

        for judge in self.proxy_judges:
            if self.send_query(url=judge) != False:
                checked_judges.append(judge)
            
        self.proxy_judges = checked_judges
        
        if len(checked_judges) == 0:
            print("ERROR: JUDGES ARE OUTDATED. CREATE A GIT BRANCH AND UPDATE SELF.PROXY_JUDGES")
            exit()
        elif len(checked_judges) == 1:
            print('WARNING! THERE\'S ONLY 1 JUDGE!')    

    def get_ip(self) -> str:
        '''
            Gets the IP checking it in https://api.ipify.org
            Return: IP or "" if it couldn't find anything
        '''
        r = self.send_query(url='https://api.ipify.org/')

        if not r:
            return ""

        return r['response']

    def send_query(self, proxy: Union[str, bool] = False,  url: str = None, tls = 1.3, \
                    user: str = None, password: str = None) -> Union[bool, dict]:
        '''
            Sends a query to a judge to get info from judge.
            Args:
                :param proxy, "IP:Port". Proxy to use in the connection
                :param url, str. Judge to use
                :param tls
                :param user, str. Username for proxy
                :param password, str. Password for proxy
            Returns: 
                False if response is not 200. Otherwise: 'timeout': timeout,'response': response}
        '''
        response = BytesIO()
        c = pycurl.Curl()
        if self.verbose:
            c.setopt(c.VERBOSE, True)

        c.setopt(c.URL, url or random.choice(self.proxy_judges))
        c.setopt(c.WRITEDATA, response)
        c.setopt(c.TIMEOUT_MS, self.timeout)

        if user is not None and password is not None:
            c.setopt(c.PROXYUSERPWD, f"{user}:{password}")            

        c.setopt(c.SSL_VERIFYHOST, 0)
        c.setopt(c.SSL_VERIFYPEER, 0)

        if proxy:
            c.setopt(c.PROXY, proxy)
            if proxy.startswith('https'):
                c.setopt(c.SSL_VERIFYHOST, 1)
                c.setopt(c.SSL_VERIFYPEER, 1)
                c.setopt(c.CAINFO, certifi.where())
                if tls == 1.3:
                    c.setopt(c.SSLVERSION, c.SSLVERSION_MAX_TLSv1_3)
                elif tls == 1.2:
                    c.setopt(c.SSLVERSION, c.SSLVERSION_MAX_TLSv1_2)
                elif tls == 1.1:
                    c.setopt(c.SSLVERSION, c.SSLVERSION_MAX_TLSv1_1)
                elif tls == 1.0:
                    c.setopt(c.SSLVERSION, c.SSLVERSION_MAX_TLSv1_0)

        # Perform request
        try:
            c.perform()
        except Exception as e:
            #print(e)
            return False

        # Return False if the status is not 200
        if c.getinfo(c.HTTP_CODE) != 200:
            return False

        # Calculate the request timeout in milliseconds
        timeout = round(c.getinfo(c.CONNECT_TIME) * 1000)

        # Decode the response content
        response = response.getvalue().decode('iso-8859-1')

        return {
            'timeout': timeout,
            'response': response
        }

    def parse_anonymity(self, r:str) -> str:
        '''
            Obtain the anonymity of the proxy
            Args:
                :param, str. IP
            Return: Transparent, Anonymous or Elite
        '''

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

    def get_country(self, ip: str) -> list:
        '''
            Checks in https://ip2c.org the country from a given IP
            Args:
                :param ip, str. Including dots, but not port
            Return: [country, country shortname Alpha-2 code]
        '''
        r = self.send_query(url='https://ip2c.org/' + ip)

        if r and r['response'][0] == '1':
            r = r['response'].split(';')
            return [r[3], r[1]]

        return ['-', '-']

    def check_proxy(self, proxy: str, check_country: bool = True, check_address: bool = False, check_all_protocols: bool = False, \
                    protocol: Union[str, list] = None, retries: int = 1, tls: float = 1.3, user: str = None, password: str = None) -> Union[bool, dict]:
        '''
        Checks if the proxy is working.
        Args:
            :param proxy, str "IP:Port", Ip including the dots.
            :param check_country, bool. Get country and country_code from https://ip2c.org/
            :param check_address, bool. Take remote adress from judge url
            :param check_all_protocols, bool. If True, after we found the proxy is of a specific \
                                        protocol, we continue looking for its validity for others. Protocols are: http, https, socks4, socks5
            :param protocol, str. 'http', 'https', 'socks4', 'socks5', or a list containing some of these. Check only these protocols
            :param retries, int. Number of times to retry the checking in case of proxy failure
            :param tls, float. 1.3, 1.2, 1.1, 1.0. If using https, this will be the maximum TLS tried in the connection. Notice that the TLS version
                    to be used will be random, but as maximum this parameter
            :param user, str. User to use for proxy connection
            :pram password, str. Password to use for proxy connection
        Return:
            False if not working. Otherwise:
            {'protocols': list of protocols available, 'anonymity': 'Anonymous' or 'Transparent' or 'Elite','timeout': timeout\
             'country': 'country', 'country_code': 'country_code', 'remote_address':'remote_address'}
        '''

        protocols = {}
        timeout = 0

        # Select protocols to check
        protocols_to_test = ['http', 'https', 'socks4', 'socks5']

        if isinstance(protocol, list):
            temp = []
            for p in protocol:
                if p in protocols_to_test:
                    temp.append(p)
            
            if len(temp) != 0:
                protocols_to_test = temp 

        elif protocol in protocols_to_test:
            protocols_to_test = [protocol]

        # Test the proxy for each protocol
        for retry in range(retries):
            for protocol in protocols_to_test:
                r = self.send_query(proxy=protocol + '://' + proxy, user=user, password=password, tls=tls)

                # Check if the request failed
                if not r:
                    continue

                protocols[protocol] = r
                timeout += r['timeout']

                if check_all_protocols == False:
                    break
            
            # Do not retry if any connection was successful
            if timeout != 0:
                break

        # Check if the proxy failed all tests
        if (len(protocols) == 0):
            return False

        r = protocols[random.choice(list(protocols.keys()))]['response']

        # Get country
        if check_country:
            country = self.get_country(proxy.split(':')[0])

        # Check anonymity
        anonymity = self.parse_anonymity(r)

        # Check timeout
        timeout = timeout // len(protocols)

        # Check remote address
        if check_address:
            remote_regex = r'REMOTE_ADDR = (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            remote_addr = re.search(remote_regex, r)
            if remote_addr:
                remote_addr = remote_addr.group(1)

        results = {
            'protocols': list(protocols.keys()),
            'anonymity': anonymity,
            'timeout': timeout
        }

        if check_country:
            results['country'] = country[0]
            results['country_code'] = country[1]

        if check_address:
            results['remote_address'] = remote_addr

        return results
