from api import Godaddy

gApi = Godaddy( KEY = 'xxxxxxxxxxxxxxxxxxxx', SECRET='xxxxxxxxxxxxxxxxxxx', DOMAIN='domain.com' )

gApi.cname( '@' , 'baidu.com' )

