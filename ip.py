#Python 2.7 / Python 3.x
from geoip import xgeoip
r = xgeoip.GeoIp()
r.load_memory()
print $1
print (r.resolve("123.44.57.4").country_code)
#This prints : {'country': 'Korea (South)', 'host_name': '', 'country_code': 'KR'}

