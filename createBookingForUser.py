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

def createBookingWithPrice(access_token, location_id,
                        start_time, slot_duration,
                        price, source, 
                        currency, bed_id, 
                        paid_by, is_instant_booking=False):
    url = "https://api-alpha-v3.mybackhug.com/api/v3/bookings/create"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "location_id": location_id,
        "start_time": start_time,
        "slot_duration": slot_duration,
        "price": price,
        "source": source,
        "currency": currency,
        "bed_id": bed_id,
        "paid_by": paid_by,
        "is_instant_booking": is_instant_booking
    }

    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code in (200, 201):
        print("Tạo booking thành công")
        print("Response JSON:", resp.json())
    else:
        try:
            print("Response JSON:", resp.json())
        except Exception:
            print("Response text:", resp.text)
        print("Tạo booking thất bại")
    return resp


def checkCreateBookingSuccess(access_token, location_id, company_id,
                  bed_id,slot_duration, start_time,
                  price, currency):
    resp = createBooking(access_token, location_id, company_id,
                  bed_id,slot_duration, start_time,
                  price, currency)
    # resp = createBooking(access_token, 821, 276, 1497, 20, "2025-12-06 14:00", 0, "VND")
    if resp.status_code in (200, 201):
        print("Tạo booking thành công cho user") 
        return True
    else: 
        print("Tạo booking thất bại cho user")
        try:
            msg = resp.json().get("message")
        except Exception:
            msg = resp.text
        print("Message:", msg)
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

def checkFailSLotIsAlreadyBooked(access_token, location_id, start_time, slot_duration,
                           price, source, currency, bed_id, paid_by, is_instant_booking=False):
    resp = createBookingWithPrice(access_token, location_id, start_time, slot_duration,
                           price, source, currency, bed_id, paid_by, is_instant_booking=False)
    if resp.status_code not in (200, 201):
        print("Tạo booking thất bại cho user")
        try:
            msg = resp.json().get("message")
        except Exception:
            msg = resp.text
        print("Message:", msg)
        assert "The selected booking slot has just been booked." in msg
        return True
    return False

# ...existing code...
def getBookingID(access_token,
                 location_id, start_time, slot_duration,
                 price, source, currency, bed_id,
                 paid_by, is_instant_booking=False):
    # create booking if needed
    booking_resp = createBookingWithPrice(
            access_token,
            location_id,
            start_time,
            slot_duration,
            price,
            source,
            currency,
            bed_id,
            paid_by,
            is_instant_booking
        )

    # normalize booking_resp to dict
    if isinstance(booking_resp, requests.Response):
        try:
            data = booking_resp.json()
        except Exception:
            print("Invalid booking response (not JSON)")
            return None
    elif isinstance(booking_resp, dict):
        data = booking_resp
    else:
        print("booking_resp must be requests.Response or dict")
        return None

    booking_id = data.get("id") or (data.get("data") and data["data"].get("id"))
    if not booking_id:
        print("No booking id found in response")
        return None

    print("Booking id:", booking_id)
    return booking_id

if __name__ == "__main__":
    email = "admin@paclamedical.com"
    password = "pacla@Robophysio2018"
    refresh_token = setup.login(email, password)
    access_token = setup.create_access_token(refresh_token)

    # create booking on behalf of user
    # access_token_behalf = getAccessTokenOnBehalfOfUser(access_token, "nhokun050+7@gmail.com")
    # checkCreateBookingSuccess(access_token_behalf, location_id=821, company_id=276,
    #                           bed_id=1497, slot_duration=20,
    #                           start_time="2025-12-06 14:00",
    #                           price=0, currency="VND")
    # checkCreateBookingFail(access_token_behalf)

    # user create booking
    email1 = "nhokun050+6@gmail.com"
    password1 = "Backhug12345"
    refresh_token1 = setup.login(email1, password1)
    access_token1 = setup.create_access_token(refresh_token1)
    # checkCreateBookingSuccess(access_token1, location_id=821, company_id=276,
    #                           bed_id=1497, slot_duration=20,
    #                           start_time="2025-12-03 19:00",
    #                           price=30000, currency="VND")

    # checkFailSLotIsAlreadyBooked(access_token1, location_id=821, 
    #                        start_time='2025-12-03 01:00', slot_duration=20,
    #                        price=30000.0, source='card_1SXQ61R1vQ08ydxFPyjRjXt9', 
    #                        currency='VND', bed_id=1497, 
    #                        paid_by='money', is_instant_booking=False)
    
    createBookingWithPrice(access_token1, location_id=821, 
                           start_time='2025-12-03 05:00', slot_duration=20,
                           price=30000.0, source='card_1SXQ61R1vQ08ydxFPyjRjXt9', 
                           currency='VND', bed_id=1497, 
                           paid_by='money', is_instant_booking=False)
    