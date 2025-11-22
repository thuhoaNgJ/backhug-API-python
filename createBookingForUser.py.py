import requests
import setup

def getAccessTokenOnBehalfOfUser(access_token, user_email):
    url = "https://paclaadmin.alphaweb.mybackhug.com/api/v3/821/admin/users/gen-token-on-behalf"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }   
    payload = {
        "email": user_email
    }       
    resp = requests.post(url, json=payload, headers=headers)
    print("Status code:", resp.status_code)
    data = resp.json()
    access_token = data.get("access_token")
    return access_token        


def createBooking(access_token, location_id, company_id,
                  bed_id,slot_duration, start_time,
                  price, currency):
    url = "https://api-alpha-v3.mybackhug.com/api/v3/bookings/create"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "location_id": location_id,
        "company_id": company_id,
        "bed_id": bed_id,
        "slot_duration": slot_duration,
        "start_time": start_time,
        "price": price,
        "currency": currency
    }

    resp = requests.post(url, json=payload, headers=headers)
    return resp

def checkCreateBookingSuccess(access_token):
    resp = createBooking(access_token, 821, 276, 1497, 20, "2025-12-06 14:00", 0, "VND")
    if resp.status_code in (200, 201):
        print("Tạo booking thành công cho user")
        return True
    return False

def checkCreateBookingFail(access_token):
    resp = createBooking(access_token, 821, 276, 1497, 20, "2025-12-07 14:00", 0, "VND")
    if resp.status_code not in (200, 201):
        print("Tạo booking thất bại cho user")
        try:
            msg = resp.json().get("message")
        except Exception:
            msg = resp.text
        print("Message:", msg)
        return True
    return False

if __name__ == "__main__":
    email = "admin@paclamedical.com"
    password = "pacla@Robophysio2018"
    refresh_token = setup.login(email, password)
    access_token = setup.create_access_token(refresh_token)

    # create booking on behalf of user
    access_token_behalf = getAccessTokenOnBehalfOfUser(access_token, "nhokun050+7@gmail.com")
    checkCreateBookingSuccess(access_token_behalf)
    checkCreateBookingFail(access_token_behalf)

    # user create booking
    email1 = "nhokun050+7@gmail.com"
    password1 = "Backhug123"
    refresh_token1 = setup.login(email1, password1)
    access_token1 = setup.create_access_token(refresh_token)
    checkCreateBookingSuccess(access_token1)