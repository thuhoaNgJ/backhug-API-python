import requests
import setup

# Create a public location named "Test location" for company_id "276"
def createNewLocation(access_token):
    url = "https://paclaadmin.alphaweb.mybackhug.com/api/v3/base/partner-locations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "currency": "VND",
        "company_id": "276",
        "status": 3,
        "location_type": "CLINIC_PUBLIC",
        "passkey_enabled": False,
        "address": {
            "city": "Hà Nội",
            "country": "Vietnam",
            "country_short_name": "VN",
            "city_short_name": "hanoi",
            "street": "102 Đ. Trần Phú, P. Mộ Lao, Hà Đông, Hà Nội, Vietnam",
            "timezone": "Asia/Ho_Chi_Minh"
        },
        "city": "Hà Nội",
        "city_short_name": "hanoi",
        "country": "Vietnam",
        "country_short_name": "VN",
        "street": "102 Đ. Trần Phú, P. Mộ Lao, Hà Đông, Hà Nội, Vietnam",
        "timezone": "Asia/Ho_Chi_Minh",
        "duration_mins": [20, 30, 40],
        "email_support": "nth.712ng@gmail.com",
        "handset_code": "007",
        "imgs": [],
        "latitude": 20.9791308,
        "longitude": 105.7855745,
        "mindbody_location_id": None,
        "name": "Test location",
        "passkey_enabled": False,
        "phone_number": "",
        "price_rules": [
            {"currency": "VND", "slot": 10, "price": 0},
            {"currency": "VND", "slot": 20, "price": 0},
            {"currency": "VND", "slot": 30, "price": 0},
            {"currency": "VND", "slot": 40, "price": 0}
        ],
        "send_noti_booking_email_partner": [2, 10, 3, 6, 4]
    }

    resp = requests.post(url, json=payload, headers=headers)
    print("Status code:", resp.status_code)
    # try:
    #     print("Response:", resp.json())
    # except Exception:
    #     print("Response text:", resp.text)
    if resp.status_code == 200:
        print("Location created successfully.")
    else:
        print("Location created fail.")
    return resp

if __name__ == "__main__":
    email = "admin@paclamedical.com"
    password = "pacla@Robophysio2018"
    refresh_token = setup.login(email, password)
    access_token = setup.create_access_token(refresh_token)
    createNewLocation(access_token)