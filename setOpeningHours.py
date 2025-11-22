import requests
import setup

def set_opening_hours(access_token, location_id="821", company_id="276"):
    url = f"https://paclaadmin.alphaweb.mybackhug.com/api/v3/location/{location_id}/list-hours"
    params = {"confirm_change_open_time": "False"}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = [
        {
            "day_of_week": "Mon",
            "location_id": location_id,
            "company_id": company_id,
            "open_time": "00:00:00",
            "close_time": "23:45:00",
            "block": [
                {"block_start_time": "12:00:00", "block_end_time": "13:00:00"}
            ]
        },
        {
            "day_of_week": "Tue",
            "location_id": location_id,
            "company_id": company_id,
            "open_time": "00:00:00",
            "close_time": "23:45:00",
            "block": []
        },
        {
            "day_of_week": "Wed",
            "location_id": location_id,
            "company_id": company_id,
            "open_time": "00:00:00",
            "close_time": "23:45:00",
            "block": []
        },
        {
            "day_of_week": "Thu",
            "location_id": location_id,
            "company_id": company_id,
            "open_time": "00:00:00",
            "close_time": "23:45:00",
            "block": []
        },
        {
            "day_of_week": "Fri",
            "location_id": location_id,
            "company_id": company_id,
            "open_time": "00:00:00",
            "close_time": "23:45:00",
            "block": []
        },
        {
            "day_of_week": "Sat",
            "location_id": location_id,
            "company_id": company_id,
            "open_time": "00:00:00",
            "close_time": "23:45:00",
            "block": []
        },
        {
            "day_of_week": "Sun",
            "location_id": location_id,
            "company_id": company_id
            # sunday is closed
        }
    ]

    resp = requests.put(url, params=params, json=payload, headers=headers)
    print("Status code:", resp.status_code)
    try:
        data = resp.json()
        print("Response JSON:", data)
    except Exception:
        data = None
        print("Response text:", resp.text)

    # check preview confirmation
    if resp.status_code == 200 and isinstance(data, dict) and data.get("confirmation") is True:
        print("Setup opening hours của location thành công.")
    else:
        print("Không thể setup opening hours của location.")
        if isinstance(data, dict):
            print("Preview confirmation:", data.get("confirmation"))
            print("Message:", data.get("message", ""))
    return resp

if __name__ == "__main__":
    email = "admin@paclamedical.com"
    password = "pacla@Robophysio2018"
    refresh_token = setup.login(email, password)
    access_token = setup.create_access_token(refresh_token)
    set_opening_hours(access_token, location_id="821", company_id="276")