import PayloadRequest
import requests

def login(username, password):
    url = "https://paclaadmin.api-alpha-v3.mybackhug.com/api/v3/auth/login"
    headers = {"Content-Type": "application/json"}
    payload = PayloadRequest.dangNhapPayload(username, password)
    response = requests.post(url, json=payload, headers=headers)
    print("Status code:", response.status_code)
    assert response.status_code == 200
    login_response = response.json()
    refresh_token = login_response.get("refresh_token")
    return refresh_token

def create_access_token(refresh_token):
    url = "https://api-alpha-v3.mybackhug.com/api/v3/auth/access_token"
    headers = {
        "Content-Type": "application/json",    
        "Token": refresh_token 
    }
    response = requests.post(url, headers=headers)
    assert response.status_code == 200
    access_token_response = response.json()
    access_token = access_token_response.get("access_token")
    return access_token

if __name__ == "__main__":
    email = "admin@paclamedical.com"
    password = "pacla@Robophysio2018"
    token = login(email, password)
    print(f"Refresh Token: {token}")
    
    access_token = create_access_token(token)
    print(f"Access Token: {access_token}")

