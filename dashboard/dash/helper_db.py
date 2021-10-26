from woocommerce import API
from datetime import datetime

wcapi = API(
    url="http://waraqata.com/", # Your store URL
    consumer_key="ck_40067fcf6aecc329b6e5fb3ee4ac8ff86a4edabd", # Your consumer key
    consumer_secret="cs_4128f8b5b5cc3a1dc62719b2d5cfc2f88f57bb7e", # Your consumer secret
    wp_api=True, # Enable the WP REST API integration
    version="wc/v3", # WooCommerce WP REST API version
    timeout=30,    
)


orders = wcapi.get("orders",params={"per_page": 100}).json()
# print(orders[0]['id'])
order_list = [[order['id'],order['billing']['first_name'],order['billing']['last_name'],order['billing']['phone'],
                order['billing']['email'],order['billing']['address_1'],order['date_created'],
                order['line_items'][0]['name'],order['line_items'][0]['quantity'],order['line_items'][0]['price'],
                int(float(order['total'])),order['date_paid'],order['payment_method_title'],order['status'],
                order['shipping_lines']] for order in orders]
                

order_list = [['1900-01-01T00:00:00' if ode is None else ode for ode in order]for order in order_list]

# order_list= [order for order in order_list]
# order_list = [[order_ship[0][0] if 'method_title' in ode else ode for ode in order]for order in order_list]
order_ship= [order[14] for order in order_list]
order_ship= [order[0]['method_title'] if len(order)==1 else 'No Delivery Information'for order in order_ship]
for i in range(len(order_ship)):
    order_list[i].append(order_ship[i])
# print(order_list)
# print(order_ship)
# print(order_ship[55][0]['method_title'])



