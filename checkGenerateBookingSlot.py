import requests
from datetime import datetime
import setup

def checkBookingSlot(access_token,
                     location_id=821,
                     date="2025-12-10",
                     slot_duration=20,
                     bed_id=1497):

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
        data = resp.json()
        print("Response JSON preview (first 5):", data[:5] if isinstance(data, list) else data)
    except Exception:
        print("Response text:", resp.text)
        data = None

    assert resp.status_code == 200

    # normalize to list of slot dicts
    slots = []
    if isinstance(data, list):
        slots = data
    elif isinstance(data, dict):
        # common alternative keys
        for k in ("data", "slots", "preview"):
            if k in data and isinstance(data[k], list):
                slots = data[k]
                break
        # fallback: try to find a list value inside dict
        if not slots:
            for v in data.values():
                if isinstance(v, list):
                    slots = v
                    break

    if not slots:
        print("No slots returned")
        return resp

    prev_dt = None
    for i, s in enumerate(slots):
        slot_time = s.get("slot_time") if isinstance(s, dict) else None
        is_available = s.get("is_available") if isinstance(s, dict) else None

        # parse ISO datetime with timezone
        try:
            dt = datetime.fromisoformat(slot_time)
        except Exception:
            # try trimming fractional seconds / fallback
            try:
                dt = datetime.fromisoformat(slot_time.replace("Z", "+00:00"))
            except Exception:
                dt = None

        print(f"{i}: slot_time={slot_time}  is_available={is_available}")

        if prev_dt and dt:
            diff_min = int((dt - prev_dt).total_seconds() / 60)
            if diff_min != 10:
                print(f"Warning: slot {i-1} -> {i} interval = {diff_min} minutes (expected 10)")
        prev_dt = dt

    return resp

if __name__ == "__main__":
    email = "admin@paclamedical.com"
    password = "pacla@Robophysio2018"
    refresh_token = setup.login(email, password)
    access_token = setup.create_access_token(refresh_token)
    checkBookingSlot(access_token)