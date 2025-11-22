import requests
import setup

def setPriceLocation(access_token, location_id):
    # id: device id from stock
    # url = "https://paclaadmin.alphaweb.mybackhug.com/api/v3/homebeds/" + str(device_id) + "/shared"
    url = f"https://paclaadmin.alphaweb.mybackhug.com/api/v3/base/partner-locations/{location_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        #choose option duration
        "duration_mins": [10, 20, 30, 40], 
        # set the price
        "price_rules": [
            {
                "slot": 10,
                "price": 30000,
                "currency": "VND",
                "location_id": location_id,
            },
            {
                "slot": 20,
                "price": 40000,
                "currency": "VND",
                "location_id": location_id,
            },
            {
                "slot": 30,
                "price": 50000,
                "currency": "VND",
                "location_id": location_id,
            },
            {
                "slot": 40,
                "price": 80000,
                "currency": "VND",
                "location_id": location_id, 
            }
        ]
    }

    resp = requests.put(url, json=payload, headers=headers)
    print("Status code:", resp.status_code)
    if resp.status_code == 200:
        print("Response JSON:", resp.json())
        print("Set price thành công cho location")
    else:
        print("Response text:", resp.text)
        print("Set price thất bại cho location")
    return resp

if __name__ == "__main__":
    email = "admin@paclamedical.com"
    password = "pacla@Robophysio2018"
    refresh_token = setup.login(email, password)
    access_token = setup.create_access_token(refresh_token)
    setPriceLocation(access_token, 821)