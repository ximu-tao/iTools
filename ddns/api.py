import json
from urllib import request


class API:
    def __init__(self):
        pass

    def cname(self , NAME , VALUE , TTL=None):
        pass

    def a(self , NAME , VALUE , TTL=None):
        pass

    def aaaa(self , NAME , VALUE , TTL=None):
        pass

    def txt(self):
        pass

    def max(self):
        pass

    def srv(self):
        pass

    def caa(self):
        pass

    def soa(self):
        pass

    def ns(self):
        pass

    def https(self):
        pass


class Godaddy(API):
    def __init__(self, KEY, SECRET, DOMAIN, TTL=60 * 60):
        self.HEADERS = {
            "Accept": "application/json",
            'Content-type': 'application/json',
            'Authorization': 'sso-key {}:{}'.format(KEY, SECRET)
        }
        self.TTL = TTL
        self.DOMAIN = DOMAIN

    def update_dns(self , TYPE , NAME, VALUE, TTL ):
        GOD_ADDY_API_URL = "https://api.godaddy.com/v1/domains/{}/records/{}/{}".format(self.DOMAIN, TYPE, NAME)
        data = json.dumps([{"data": VALUE, "name": NAME, "ttl": self.TTL, "type": TYPE}]).encode('utf-8')
        # print( GOD_ADDY_API_URL )
        req = request.Request(url=GOD_ADDY_API_URL, data=data, headers=self.HEADERS, method='PUT')
        with request.urlopen(req) as response:
            pass
        return VALUE if not response.read().decode('utf-8') else VALUE

    def cname(self , NAME , VALUE , TTL=None):
        self.update_dns( 'CNAME' , NAME , VALUE , TTL= TTL if TTL else self.TTL)

    def a(self , NAME , VALUE , TTL=None):
        self.update_dns( 'A' , NAME , VALUE , TTL= TTL if TTL else self.TTL)

    def aaaa(self , NAME , VALUE , TTL=None):
        self.update_dns( 'AAAA' , NAME , VALUE , TTL= TTL if TTL else self.TTL)


