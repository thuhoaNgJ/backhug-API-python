import createBookingForUser 
import requests
from datetime import datetime
import setup

def checkBookingSlot(access_token, location_id, date,slot_duration, bed_id):
    url = "https://paclaadmin.alphaweb.mybackhug.com/api/v3/bookings/generate-slot-time"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "location_id": location_id,
        "date": date,
        "slot_duration": slot_duration,
        "bed_id": bed_id
    }

    resp = requests.post(url, json=payload, headers=headers)
    print("Status code:", resp.status_code)
    try:
        print("Done run request")
        # print("Response JSON:", resp.json())
    except Exception:
        print("Response text:", resp.text)
    return resp

def checkCloseDate(access_token, location_id=821, bed_id=1497, slot_duration=20, closed_date="2025-12-07"):

    resp = checkBookingSlot(access_token,location_id, bed_id, slot_duration, closed_date)

    try:
        data = resp.json()
        msg = data.get("message", "") if isinstance(data, dict) else str(data)
        print("Response JSON:", data)
    except Exception:
        msg = resp.text
        print("Response text:", msg)

    assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
    assert "is not available on the selected day" in msg, f"Expected message to contain target text, got: {msg}"
    return resp

def checkGapTimeSlot(access_token, location_id, date, slot_duration, bed_id):
    resp = checkBookingSlot(access_token, location_id, date, slot_duration, bed_id)
    if resp.status_code != 200:
        print("No slot available")
        return []
    data = resp.json()
    
    expected_gap = slot_duration - 10  # phút
    wrong_slots = []

    for i in range(1, len(data)):
        prev = datetime.fromisoformat(data[i - 1]["slot_time"])
        curr = datetime.fromisoformat(data[i]["slot_time"])

        slot_gap = (curr - prev).total_seconds() / 60  # phút

        if slot_gap != expected_gap:
            wrong_slots.append({
                "index": i,
                "previous_slot": data[i - 1],
                "current_slot": data[i],
                "gap_minutes": slot_gap
            })
    print("Wrong slots with unexpected gaps:", wrong_slots)
    return wrong_slots

if __name__ == "__main__":
    email = "admin@paclamedical.com"
    password = "pacla@Robophysio2018"
    refresh_token = setup.login(email, password)
    access_token = setup.create_access_token(refresh_token)
    # đặt lịch cho user
    start_time = "2025-12-06 15:00"
    slot_duration=20
    access_token_behalf = createBookingForUser.getAccessTokenOnBehalfOfUser(access_token, "nhokun050+7@gmail.com")
    createBookingForUser.checkCreateBookingSuccess(access_token_behalf, 
                                    location_id=821, company_id=276,
                                    bed_id=1497, slot_duration=20,
                                    start_time="2025-12-06 15:00",
                                    price=0, currency="VND")
     # check closedate on Sunday -> no slot generated
    # checkCloseDate(access_token, location_id=821, bed_id=1497, 
    #                slot_duration=20, closed_date="2025-12-07")
   
    # checkBookingSlot(access_token, location_id=821, bed_id=1497,
    #                   date="2025-12-05", slot_duration=20)
    
    checkGapTimeSlot(access_token, location_id=821, bed_id=1497,
                      date="2025-12-06", slot_duration=20)
    