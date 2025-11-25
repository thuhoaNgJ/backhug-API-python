import requests
import json
import setup
import createBookingForUser

def getListFirstPromotionOfLocation(access_token, location_id, city_id, country_id):
    """
    Fetch location info and print/return list of user_ids_used from first_promotion.
    """
    url = "https://api-alpha-v3.mybackhug.com/api/v3/location"
    filter_list = [
        {"field": "city_id", "op": "eq", "value": city_id},
        {"field": "country_id", "op": "eq", "value": country_id},
        {"field": "id", "op": "eq", "value": location_id},
        {"field": "deleted", "op": "eq", "value": False}
    ]
    params = {
        "id": location_id,
        "filter": json.dumps(filter_list)
    }
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}

    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        print("Unexpected status code:", resp.status_code)
        try:
            print("Response JSON:", resp.json())
        except Exception:
            print("Response text:", resp.text)
        return []

    data = resp.json()
    locations = data.get("data", [])
    user_ids = []
    for loc in locations:
        for promo in loc.get("first_promotion", []):
            user_ids.extend(promo.get("user_ids_used", []))

    print("user_ids_used:", user_ids)
    return user_ids

def checkUserInFirstPromotion(access_token, user_id, location_id=821, city_id=1, country_id=1):
    user_ids = getListFirstPromotionOfLocation(access_token, location_id, city_id, country_id)
    try:
        target = int(user_id)
    except Exception:
        target = user_id

    found = False
    for uid in user_ids:
        try:
            if int(uid) == target:
                found = True
                break
        except Exception:
            if uid == target:
                found = True
                break

    if found:
        print(f"{user_id} đã sử dụng first_promotion")
    else:
        print(f"{user_id} chưa sử dụng first_promotion")

    return found


if __name__ == "__main__":
    email = "admin@paclamedical.com"
    password = "pacla@Robophysio2018"
    refresh_token = setup.login(email, password)
    access_token = setup.create_access_token(refresh_token)
    getListFirstPromotionOfLocation(access_token, location_id=821, city_id=1, country_id=1)
    
    # check user không có trong first promotion vì user chưa có booking
    checkUserInFirstPromotion(access_token, user_id=1974, location_id=821, city_id=1, country_id=1)

    # user tự tạo booking
    email1 = "nhokun050+6@gmail.com"
    password1 = "Backhug12345"
    refresh_token_user = setup.login(email1, password1)
    access_token_user = setup.create_access_token(refresh_token_user)
    createBookingForUser.checkCreateBookingSuccess(access_token_user, location_id=821, company_id=276,
                              bed_id=1497, slot_duration=20,
                              start_time="2025-12-06 20:00",
                              price=0, currency="VND")
    
    # check user đã có trong first promotion vì user đã có booking
    checkUserInFirstPromotion(access_token, user_id=1974, location_id=821, city_id=1, country_id=1)
    