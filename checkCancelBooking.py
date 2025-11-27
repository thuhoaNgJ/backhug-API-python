import requests
import setup
import createBookingForUser

def runRequestCancel(access_token, booking_id):
    url = f"https://api-alpha-v3.mybackhug.com/api/v3/bookings/cancel/{booking_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    resp = requests.post(url, headers=headers)

    if resp.status_code != 200:
        try:
            print("Response JSON:", resp.json())
        except Exception:
            print("Response text:", resp.text)
        print("Cancel booking thất bại")
    else:
        print("Cancel booking thành công")

    return resp

if __name__ == "__main__":
    email = "admin@paclamedical.com"
    password = "pacla@Robophysio2018"
    refresh_token = setup.login(email, password)
    access_token = setup.create_access_token(refresh_token)

    email_user = "nhokun050+6@gmail.com"
    password_user = "Backhug12345"
    refresh_token_user = setup.login(email_user, password_user)
    access_token_user = setup.create_access_token(refresh_token_user)

    booking_id = createBookingForUser.getBookingID(access_token_user, location_id=821, 
                           start_time='2025-12-04 05:00', slot_duration=20,
                           price=30000.0, source='card_1SXQ61R1vQ08ydxFPyjRjXt9', 
                           currency='VND', bed_id=1497, 
                           paid_by='money', is_instant_booking=False)
    # admin cancel booking
    # runRequestCancel(access_token, booking_id) 

    # user cancel booking
    runRequestCancel(access_token_user, booking_id) 
    