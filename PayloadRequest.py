
def dangNhapPayload(username, password):
    return {
        "email": username,
        "password": password
    }

def taoCompanyPayload(name, address, domain, company_type, country,
                    country_short_name, city, city_short_name, timezone):
    return {
        "name": name,
        "address": address,
        "domain": domain,
        "company_type": company_type,
        "country": country,
        "country_short_name": country_short_name,
        "city": city,
        "city_short_name": city_short_name,
        "timezone": timezone
    }

