from datetime import datetime, time
from pytz import timezone
from woocommerce import API

test = [[1,2,3,None],[2,3,4]]
tester = [[t**2 if t==2 else t for t in tt]for tt in test]
ter = datetime.fromisoformat('2020-10-12T15:07:01')
lagos = timezone('Africa/Lagos')
# print(datetime.datetime(ter, tzinfo = pytz.))
# print(str(lagos.localize(datetime.fromisoformat('1900-01-01T00:00:00'))))

# wcapi = API(
#         url="http://waraqata.com/", # Your store URL
#         consumer_key="ck_40067fcf6aecc329b6e5fb3ee4ac8ff86a4edabd", # Your consumer key
#         consumer_secret="cs_4128f8b5b5cc3a1dc62719b2d5cfc2f88f57bb7e", # Your consumer secret
#         wp_api=True, # Enable the WP REST API integration
#         version="wc/v3",# WooCommerce WP REST API version
#         query_string_auth=True,  
#         timeout=30)

# data = {
#     "status": "on-hold"
#     }
# r = wcapi.post("orders/4739",data)
# print(r.status_code)
# print(r.json())
from pathlib import Path


p = [4,4,5,'+']

res = []
for i in range(len(p)):
    if type(p[i]) is int:
        res.append(p[i])
    if p[i] == '+':
        res.append(res[-1]*2)

print(res)
for b in p:
    print(b)