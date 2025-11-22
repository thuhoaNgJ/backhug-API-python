import requests
import setup

def add_users_bulk(access_token, location_id, emails, user_type, skip_add_users=False):
    url = f"https://paclaadmin.alphaweb.mybackhug.com/api/v3/{location_id}/admin/users/bulk-text"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    if isinstance(emails, str):
        emails_str = emails
        emails_list = [e.strip() for e in emails.split(",") if e.strip()]
    else:
        emails_list = [e.strip() for e in emails if isinstance(e, str) and e.strip()]
        emails_str = ", ".join(emails_list)

    payload = {
        "emails": emails_str,
        "skip_add_users": skip_add_users,
        "user_type": user_type
    }

    resp = requests.post(url, json=payload, headers=headers)
    print("Status code:", resp.status_code)

    assert resp.status_code == 200
    data = resp.json()
    added = []
    if isinstance(data, dict):
        added = data.get("added") or []

    if all(email in added for email in emails_list):
        print("Add tất cả user thành công")
    else:
        missing = [email for email in emails_list if email not in added]
        print("Không add được một số email:", missing)

    return resp

if __name__ == "__main__":
    email = "admin@paclamedical.com"
    password = "pacla@Robophysio2018"
    refresh_token = setup.login(email, password)
    access_token = setup.create_access_token(refresh_token)

    location_id = 821
    emails = ["nhokun050+6@gmail.com", "nhokun050+7@gmail.com"]
    user_type = "PREMIUM_MEMBER" #free to use member
    add_users_bulk(access_token, location_id, emails, user_type, skip_add_users=False)