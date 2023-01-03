import json
from urllib import request


class API:
    def __init__(self):
        pass

    def cname(self, NAME, VALUE, TTL=None):
        pass

    def a(self, NAME, VALUE, TTL=None):
        pass

    def aaaa(self, NAME, VALUE, TTL=None):
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

    def update_dns(self, TYPE, NAME, VALUE, TTL=60 * 60):
        GOD_ADDY_API_URL = "https://api.godaddy.com/v1/domains/{}/records/{}/{}".format(self.DOMAIN, TYPE, NAME)
        data = json.dumps([{"data": VALUE, "name": NAME, "ttl": TTL, "type": TYPE}]).encode('utf-8')
        # print( GOD_ADDY_API_URL )
        req = request.Request(url=GOD_ADDY_API_URL, data=data, headers=self.HEADERS, method='PUT')
        with request.urlopen(req) as response:
            pass
        return VALUE if not response.read().decode('utf-8') else VALUE

    def cname(self, NAME, VALUE, TTL=None):
        self.update_dns('CNAME', NAME, VALUE, TTL=TTL if TTL else self.TTL)

    def a(self, NAME, VALUE, TTL=None):
        self.update_dns('A', NAME, VALUE, TTL=TTL if TTL else self.TTL)

    def aaaa(self, NAME, VALUE, TTL=None):
        self.update_dns('AAAA', NAME, VALUE, TTL=TTL if TTL else self.TTL)


class CloudFlare(API):
    def __init__(self, API_TOKEN, Zone_ID, DOMAIN, TTL=60 * 60):
        self.HEADERS = {
            "Accept": "application/json",
            'Content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(API_TOKEN)
        }
        self.TTL = TTL
        self.Zone_ID = Zone_ID
        self.DOMAIN = DOMAIN
        self.API_URL = 'https://api.cloudflare.com/client/v4/zones/{}/dns_records'.format(self.Zone_ID)
        self.domains = self.get_all_record_id()

    def get_all_record_id(self):
        req = request.Request(
            self.API_URL,
            headers=self.HEADERS, method='GET')

        resp = request.urlopen(req).read().decode('utf-8')

        if not json.loads(resp)['success']:
            return None

        return json.loads(resp)['result']

    def get_record_id(self, NAME, only_types=None):
        print(self.domains)
        for domain in self.domains:
            if NAME == domain['name']:
                if only_types is None:
                    return domain['id']
                else:
                    if domain['type'] in only_types:
                        return domain['id']

        return None

    def update_dns(self, TYPE, NAME, VALUE, TTL=60 * 60, proxied=False, only_types: list = None, METHOD='PUT'):
        """
        默认情况下会更新DNS记录，如果该DNS记录不存在，会新建一条记录

        如果不希望误修改 MX 或 TXT 记录，可传入一个 only_types 类型 列表，比如 ['A' , 'AAAA' ],表示只在这两种类型找到一个可更新的记录
        如果没有找到符合条件的记录，会新建一条记录

        :param TYPE:
        :param NAME:
        :param VALUE:
        :param TTL:
        :param proxied: cloudflare 专有，是否启用代理
        :param only_types: 仅在该列表中寻找可更新的记录
        :param METHOD: 如果不希望更新原有记录，可传入 'POST'
        :return:
        """

        if NAME == '@':
            NAME = self.DOMAIN
        else:
            NAME = '%s.%s' % (NAME, self.DOMAIN)

        DOMAIN_ID = ''

        if METHOD == 'PUT':
            DOMAIN_ID = self.get_record_id(NAME, only_types)

        if DOMAIN_ID is None:
            METHOD = 'POST'
            DOMAIN_ID = ''

        print(DOMAIN_ID)
        API_URL = "{}/{}".format(self.API_URL, DOMAIN_ID)
        data = json.dumps({"content": VALUE, "name": NAME, "ttl": TTL, "type": TYPE, 'proxied': proxied}).encode(
            'utf-8')
        print(data)
        # print( GOD_ADDY_API_URL )
        req = request.Request(url=API_URL, data=data, headers=self.HEADERS, method=METHOD)
        with request.urlopen(req) as response:
            pass
        return VALUE if not response.read().decode('utf-8') else VALUE

    def cname(self, NAME, VALUE, TTL=None, proxied=False , only_types=None):
        self.update_dns('CNAME', NAME, VALUE, TTL=TTL if TTL else self.TTL , proxied=proxied ,  only_types=only_types if only_types else ['CNAME'])

    def a(self, NAME, VALUE, TTL=None, proxied=False , only_types=None):
        self.update_dns('A', NAME, VALUE, TTL=TTL if TTL else self.TTL , proxied=proxied,  only_types=only_types if only_types else ['A'])

    def aaaa(self, NAME, VALUE, TTL=None, proxied=False , only_types=None):
        self.update_dns('AAAA', NAME, VALUE, TTL=TTL if TTL else self.TTL , proxied=proxied, only_types=only_types if only_types else ['AAAA'] )
