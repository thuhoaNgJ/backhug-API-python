import requests
from datetime import datetime
import setup

def _parse_iso_datetime(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except Exception:
        try:
            return datetime.fromisoformat(s.replace("Z", "+00:00"))
        except Exception:
            return None

def _extract_slots_from_response(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("data", "slots", "preview"):
            if key in data and isinstance(data[key], list):
                return data[key]
        for v in data.values():
            if isinstance(v, list):
                return v
    return []

def checkBookingSlot(access_token,
                     location_id=821,
                     date="2025-12-07",
                     slot_duration=20,
                     bed_id=1497):
    url = "https://paclaadmin.alphaweb.mybackhug.com/api/v3/bookings/generate-slot-time"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
    payload = {"location_id": location_id, "date": date, "slot_duration": slot_duration, "bed_id": bed_id}

    resp = requests.post(url, json=payload, headers=headers)
    print("Status code:", resp.status_code)

    try:
        data = resp.json()
    except Exception:
        print("Response text:", resp.text)
        data = None

    if resp.status_code != 200:
        print("Unexpected status code:", resp.status_code)
        try:
            print("Response JSON:", resp.json())
            print("Failed to generate booking slots.") 
        except Exception:
            print("Response text:", resp.text)
        return resp   

    assert resp.status_code == 200

    slots = _extract_slots_from_response(data)
    if not slots:
        print("No slots returned")
        return resp

    prev_dt = None
    for i, s in enumerate(slots):
        slot_time = s.get("slot_time") if isinstance(s, dict) else None
        is_available = s.get("is_available") if isinstance(s, dict) else None

        dt = _parse_iso_datetime(slot_time)
        print(f"{i}: slot_time={slot_time}  is_available={is_available}")

        if prev_dt and dt:
            diff_min = int((dt - prev_dt).total_seconds() / 60)
            if diff_min != 10:
                print(f"Warning: interval between slot {i-1} and {i} is {diff_min} minutes (expected 10)")

        prev_dt = dt

    return resp




def checkCloseDate(access_token, location_id=821, bed_id=1497, slot_duration=20, closed_date="2025-12-07"):

    resp = checkBookingSlot(access_token,
                            location_id=location_id,
                            date=closed_date,
                            slot_duration=slot_duration,
                            bed_id=bed_id)

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

if __name__ == "__main__":
    email = "admin@paclamedical.com"
    password = "pacla@Robophysio2018"
    refresh_token = setup.login(email, password)
    access_token = setup.create_access_token(refresh_token)
    checkBookingSlot(access_token)
    