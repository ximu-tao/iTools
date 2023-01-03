import socket
from urllib import request

# 一些一般不用修改的参数

# 公网IPv4 API
CHECK_IPV4_URL = 'https://api.ipify.org'

# 公网IPv6 API
CHECK_IPV6_URL = 'https://api6.ipify.org'


def get_public_ip(api_url):
    return request.urlopen(api_url).read().decode('utf-8')


def get_public_ipv4():
    return get_public_ip(CHECK_IPV4_URL)


def get_public_ipv6():
    return get_public_ip(CHECK_IPV6_URL)


def get_local_ipv4():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('baidu.com', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


if __name__ == '__main__':
    # print(socket.gethostbyname_ex(socket.gethostname())
    print( 'public ipv4:' , get_public_ipv4() )
    print( 'public ipv6:' , get_public_ipv6() )
    print( 'local ipv4:' ,  get_local_ipv4() )