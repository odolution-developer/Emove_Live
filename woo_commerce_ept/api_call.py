import requests
import json
from requests.auth import HTTPBasicAuth

# url = "https://testing.emovedistribution.com/wp-json/wc/v3/orders/10070259"

# payload = json.dumps({
#   "status": "776incom"
# })

# customer_key = "ck_af5a26ecf4a06bd67e35c32f17e3b03a4e3b6d41"
# client_secret = "cs_6fb112632f7199ec888b741ad7792f8440b3c467"
# headers = {
#   'Content-Type': 'application/json',
#   'Cookie': 'wfwaf-authcookie-84f2384f6cdb580db54deed43039012c=5124%7Cadministrator%7Cmanage_options%2Cunfiltered_html%2Cedit_others_posts%2Cupload_files%2Cpublish_posts%2Cedit_posts%2Cread%7C51db3695185744133673a109f4e9aa306867ef0d035b4c7f714642953b670cc5'
# }

# response = requests.request("PUT", url, headers=headers, data=payload, auth=HTTPBasicAuth(customer_key, client_secret))

# print(response.text)

# WooCommerce API credentials
CUSTOMER_KEY = "ck_af5a26ecf4a06bd67e35c32f17e3b03a4e3b6d41"
CLIENT_SECRET = "cs_6fb112632f7199ec888b741ad7792f8440b3c467"


def update_order_status(order_id, status):
    url = f"https://testing.emovedistribution.com/wp-json/wc/v3/orders/{order_id}"
    
    payload = json.dumps({
        "status": status
    })
    
    headers = {
        'Content-Type': 'application/json',
        # Cookie is optional if not doing browser-authenticated requests
    }

    response = requests.put(
        url,
        headers=headers,
        data=payload,
        auth=HTTPBasicAuth(CUSTOMER_KEY, CLIENT_SECRET)
    )
    # return response.status_code

    if response.status_code in (200, 201):
        print(f"Order {order_id} updated to status: {status}")
    else:
        print(f"Failed to update order {order_id}. Status Code: {response.status_code}")
        print(response.text)
status = "220perparation_"
update_order_status(15934, status)
        
def fetch_order_status(order_id):
    url = f"https://testing.emovedistribution.com/wp-json/wc/v3/orders/{order_id}"
    
    
    headers = {
        'Content-Type': 'application/json',
        # Cookie is optional if not doing browser-authenticated requests
    }

    response = requests.get(
        url,
        headers=headers,
        auth=HTTPBasicAuth(CUSTOMER_KEY, CLIENT_SECRET)
    )

    if response.status_code in (200, 201):
        try:
            data = response.json()
            status = data.get('status', '')
            return status
        except ValueError:
            print("Response is not valid JSON:")
            print(response.text)
            return None
    else:
        print(f"Failed to fetch order {order_id}. Status Code: {response.status_code}")
        print("Response content:")
        print(response.text)
        return None

def create_coupon(code, amount, qty):
    url = "https://testing.emovedistribution.com/wp-json/wc/v3/coupons"

    payload = json.dumps({
    "code": code,
    "discount_type": "percent",
    "amount": str(amount),
    "individual_use": True,
    "exclude_sale_items": True,
    "minimum_amount": str(amount * qty)
    })
    headers = {
    'Content-Type': 'application/json',
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, auth=HTTPBasicAuth(CUSTOMER_KEY, CLIENT_SECRET))

        if response.status_code in (200, 201):
            print("Coupon created successfully:")
            print(str(response))
        else:
            print(f"Failed to create coupon. Status code: {response.status_code}")
            print("Response content:")
            # print(response.text)

    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:")
        print(e)


# create_coupon("ABC-12", 100, 2)


def fetch_coupon(coupon_id):
    url = f"https://testing.emovedistribution.com/wp-json/wc/v3/coupons/{coupon_id}"
    
    
    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.put(
        url,
        headers=headers,
        auth=HTTPBasicAuth(CUSTOMER_KEY, CLIENT_SECRET)
    )

    if response.status_code in (200, 201):
        print(f"Coupon {coupon_id} ")
    else:
        print(f"Failed to fetch coupon ")
        print(response.text)

 
# fetch_coupon(10070226)