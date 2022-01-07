from datetime import datetime, time
from pytz import timezone
from woocommerce import API

wcapi = API(
    url="http://waraqata.com/", # Your store URL
    consumer_key="ck_40067fcf6aecc329b6e5fb3ee4ac8ff86a4edabd", # Your consumer key
    consumer_secret="cs_4128f8b5b5cc3a1dc62719b2d5cfc2f88f57bb7e", # Your consumer secret
    wp_api=True, # Enable the WP REST API integration
    version="wc/v3", # WooCommerce WP REST API version
    timeout=30,    
)

products = wcapi.get("products",params={"per_page": 100}).json()
product_list = [[int(product['id']),product['name'],product['price'],product['stock_status']] for product in products if product['status'] == 'publish']
product_list = [[0 if ode == '' else ode for ode in order]for order in product_list]
product_list = [[prod[0],prod[1],float(prod[2]),prod[3]] for prod in product_list]
# print(product_list)
