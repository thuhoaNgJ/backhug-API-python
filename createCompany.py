import requests
import setup
import PayloadRequest

def createNewCompany(access_token, name, address, domain, company_type, country,
                    country_short_name, city, city_short_name, timezone):
    url = "https://paclaadmin.alphaweb.mybackhug.com/api/v3/base/companies"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = PayloadRequest.taoCompanyPayload(
        name, address, domain, company_type, country,
        country_short_name, city, city_short_name, timezone
    )
    response = requests.post(url, json=payload, headers=headers)
    print("Status code:", response.status_code)
    # try:
    #     print("Response:", response.json())
    # except Exception:
    #     print("Response text:", response.text)
    if response.status_code == 200:
        print("Company created successfully.")
    else:
        print("Failed to create company.")

if __name__ == "__main__":
    email = "admin@paclamedical.com"
    password = "pacla@Robophysio2018"

    # assign variables (example values)
    name = "auto test"
    address = "my address"
    domain = "auto-test-12345"
    company_type = "STANDARD"
    country = "Vietnam"
    country_short_name = "VN"
    city = "Ha Noi"
    city_short_name = "hanoi"
    timezone = "Asia/Ho_Chi_Minh"

    refresh_token = setup.login(email, password)
    access_token = setup.create_access_token(refresh_token)

    createNewCompany(access_token, name, address, domain, company_type, country,
                    country_short_name, city, city_short_name, timezone)
