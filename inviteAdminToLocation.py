import requests
import setup

def inviteAdminRequest(access_token, invite_email, invite_resource, invite_resource_id, role):
    url = "https://paclaadmin.alphaweb.mybackhug.com/api/v3/base/invitations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "email": invite_email,
        "invite_resource": invite_resource,
        "invite_resource_id": invite_resource_id,
        "role": role
    }

    resp = requests.post(url, json=payload, headers=headers)
    print("Status code:", resp.status_code)
    try:
        print("Response JSON:", resp.json())
    except Exception:
        print("Response text:", resp.text)
    return resp

def invite_success(access_token, invite_email, invite_resource, invite_resource_id, role):
    resp = inviteAdminRequest(access_token, invite_email, invite_resource, invite_resource_id, role)
    # ROLE_SUPER_ADMIN = 1600
    # ROLE_ADMIN = 1601

    if resp.status_code == 200:
        if role == ROLE_SUPER_ADMIN:
            role_name = "company super admin"
        elif role == ROLE_ADMIN:
            role_name = "company admin"
        else:
            role_name = str(role)
        print(f"{invite_email} được mời là {role_name} của location {invite_resource_id}")
    return resp

def invite_fail_company_super_admin(access_token, invite_email, invite_resource, invite_resource_id):
    resp = inviteAdminRequest(access_token, invite_email, invite_resource, invite_resource_id, ROLE_SUPER_ADMIN)
    if resp.status_code == 400:
        try:
            print("Response JSON:", resp.json())
        except Exception:
            print("Response text:", resp.text)
        print("Invite fail vì company đã tồn tại company_super_admin")
    else:
        print(f"Expected status 400 but got {resp.status_code}")
    return resp

def invite_location_admin(access_token):
    resp = inviteAdminRequest(access_token, email, invite_resource, invite_resource_id, ROLE_LOCATION_ADMIN)
    if resp.status_code == 200:
        print(f"Mời thành công {email} thành location admin của location id {invite_resource_id}")
    else:
        print(f"Invite failed with status {resp.status_code}")
    if resp.status_code == 200:
        print(f"Mời thành công {email} thành location admin của location id {invite_resource_id}")
    else:
        print(f"Invite failed with status {resp.status_code}")
    return resp

if __name__ == "__main__":
    email = "admin@paclamedical.com"
    password = "pacla@Robophysio2018"
    refresh_token = setup.login(email, password)
    access_token = setup.create_access_token(refresh_token)

    # biến gán
    invite_email1 = "nhokun050@gmail.com"
    invite_email2 = "nhokun051@gmail.com"
    invite_email3 = "hoanguyen@vais.vn"
    invite_resource = "companies"
    invite_resource_id = "237"  # company id
    ROLE_SUPER_ADMIN = 1600
    ROLE_ADMIN = 1601
    ROLE_LOCATION_ADMIN = 1604

    invite_resource_location = "partner-locations"
    invite_location_id = "767" 

    invite_success(access_token, invite_email1, invite_resource, invite_resource_id, ROLE_SUPER_ADMIN)
    invite_success(access_token, invite_email2, invite_resource, invite_resource_id, ROLE_ADMIN)

    invite_fail_company_super_admin(access_token, invite_email1, invite_resource, invite_resource_id)
    invite_location_admin(access_token, invite_email3, invite_resource_location, invite_location_id, ROLE_LOCATION_ADMIN)