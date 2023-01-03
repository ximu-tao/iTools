from api import Godaddy
from api import CloudFlare

gApi = Godaddy( KEY = 'xxxxxxxxxxxxxxxxxxxx', SECRET='xxxxxxxxxxxxxxxxxxx', DOMAIN='domain.com' )

gApi.cname( '@' , 'baidu.com' )


cfApi = CloudFlare( API_TOKEN='xxxxxxxxxxxxxxxxxxxx' , Zone_ID='xxxxxxxxxxxxxxxxxxxx', DOMAIN='domain.com')

cfApi.update_dns( TYPE='A' , NAME='qwe' , VALUE='192.168.7.1'  )

cfApi.a( '@' , VALUE='192.167.1.1')