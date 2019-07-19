import sys
import requests
import random
from primary_roletype import PrimaryRoleType

class DataGenerator:
    def __init__(self):
        pass
    
    def get_company(vat, country="dk"):
        req = requests.get(f"https://cvrapi.dk/api?vat={vat}&country={country}")

        if (req.status_code < 200 and req.status_code > 201):
            print("Dunno what happened")
            print(req.text)
            return None

        requestedCompany = req.json()
        # from companies import democompanies
        # if vat == 35783482:
        #     requestedCompany = democompanies[0]
        # elif vat == 19766241:
        #     requestedCompany = democompanies[1]
        # elif vat == 32939635:
        #     requestedCompany = democompanies[2]
        # elif vat == 17571559:
        #     requestedCompany = democompanies[3]

        if ("error" in requestedCompany):
            print("CVR API Error:", requestedCompany["message"])
            sys.exit(-1)

        company = {
            "vat": requestedCompany["vat"],
            "name": requestedCompany["name"],
            "pno": "0",
            "address": {
                "street": requestedCompany["address"],
                "city": requestedCompany["city"],
                "zipCode": requestedCompany["zipcode"],
                "no": -1,
                "country": "Danmark"
            }
        }

        prod_units = []

        for reqPu in requestedCompany['productionunits']:
            pu = {
                "pno": reqPu["pno"],
                "name": reqPu["name"],
                "company": {
                    "vat": vat
                },
                "address": {
                    "street": requestedCompany["address"],
                    "city": requestedCompany["city"],
                    "zipCode": requestedCompany["zipcode"],
                    "no": -1,
                    "country": "Danmark"
                }
            }

            prod_units.append(pu)

        return company, prod_units
    
    def demo_user():
        return {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "phone": "+4512345678",
            "userName": "jd",
            "password": "SecurePassword",
            "primaryRole": PrimaryRoleType.BOOKER.value
        }

    def q_user():
        return {
            "firstName": "Q",
            "lastName": "Qsen",
            "email": "q.qsen@q-er-godt.dk",
            "phone": "+4512345678",
            "userName": "q",
            "password": "q",
            "primaryRole": PrimaryRoleType.SUBSTITUTE.value
        }

    def random_users(count):
        url = f"https://randomuser.me/api/?inc=name,email,login,phone,location&nat=dk&results={count}"

        reqUsers = requests.get(url).json()["results"]
        users = []

        for reqUser in reqUsers:
            users.append({
                "firstName": reqUser["name"]["first"].title(),
                "lastName": reqUser["name"]["last"].title(),
                "email": reqUser["email"],
                "phone": reqUser["phone"],
                "userName": reqUser["login"]["username"],
                "password": reqUser["login"]["password"],
                "primaryRole": random.randint(0, 2),
                "address": {
                    "street": reqUser["location"]["street"],
                    "zipCode": reqUser["location"]["postcode"],
                    "city": reqUser["location"]["city"],
                    "state": reqUser["location"]["state"],
                    "country": "Denmark",
                    "no": random.randint(0, 199)
                }
            })
        return users

if __name__ == "__main__":
    print("Fetching from CVR:")
    company,_ = DataGenerator.get_company(35783482) # Wiberg Tech
    print("-", company["name"])
    company,_ = DataGenerator.get_company(19766241) # PST
    print("-", company["name"])
    company,_ = DataGenerator.get_company(32939635) # IT Minds
    print("-", company["name"])
    company,_ = DataGenerator.get_company(30060946) # DTU
    print("-", company["name"])
    print("Test users:")
    print(DataGenerator.random_users(4))