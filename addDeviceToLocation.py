import requests
import setup

def addDevice(access_token, device_id, location_id):
    # id: device id from stock
    # url = "https://paclaadmin.alphaweb.mybackhug.com/api/v3/homebeds/" + str(device_id) + "/shared"
    url = f"https://paclaadmin.alphaweb.mybackhug.com/api/v3/homebeds/{device_id}/shared"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "name": "Backhug auto",
        "pcb_serial_number": "",
        "hardware_id": 37,
        "device_type": "Testing",
        "partner_location_id": location_id,
        "installation_date": "2025-07-02T16:09:17.000Z",
        "description": "4th Floor",
        "is_disabled": False,
        "customer_name": "Hoa Test"
    }

    resp = requests.put(url, json=payload, headers=headers)
    print("Status code:", resp.status_code)
    try:
        print("Response JSON:", resp.json())
    except Exception:
        print("Response text:", resp.text)
    return resp

def addDeviceReport(access_token, device_id, location_id):
    resp = addDevice(access_token, device_id, location_id)
    if resp.status_code == 200:
        print("Thêm device thành công vào location")
    else:
        print(f"Thêm device thất bại với status {resp.status_code}")
        data = resp.json()
        message = data.get("message")
        print("Response:", message)

if __name__ == "__main__":
    email = "admin@paclamedical.com"
    password = "pacla@Robophysio2018"
    refresh_token = setup.login(email, password)
    access_token = setup.create_access_token(refresh_token)
    addDeviceReport(access_token, 2269, 821)
    addDeviceReport(access_token, 2269, 821)  # Thêm lại device đã thêm trước đó